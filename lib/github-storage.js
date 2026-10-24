import {
  CHUNKED_ROOT,
  CHUNKED_TAG_PREFIX,
  parseChunkedManifest,
  toChunkedArchive,
} from './chunked-archive.js';
import { toPublicFile } from './file-utils.js';
import {
  RELEASE_TAG_PREFIX,
  serializeReleaseMetadata,
  toReleaseArchive,
} from './release-archive.js';

export class GitHubStorage {
  constructor({
    token,
    owner,
    repo,
    branch = 'main',
    apiUrl = 'https://api.github.com',
    uploadUrl = 'https://uploads.github.com',
    fetchImpl = fetch,
    retryDelayMs = 1000,
  }) {
    this.token = token;
    this.owner = owner;
    this.repo = repo;
    this.branch = branch;
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.uploadUrl = uploadUrl.replace(/\/$/, '');
    this.fetch = fetchImpl;
    this.retryDelayMs = retryDelayMs;
  }

  get repositoryUrl() {
    return `https://github.com/${this.owner}/${this.repo}`;
  }

  get repositoryApiPath() {
    return `/repos/${encodeURIComponent(this.owner)}/${encodeURIComponent(this.repo)}`;
  }

  contentApiPath(path, includeRef = true) {
    const encodedPath = path.split('/').map(encodeURIComponent).join('/');
    const query = includeRef ? `?ref=${encodeURIComponent(this.branch)}` : '';
    return `${this.repositoryApiPath}/contents/${encodedPath}${query}`;
  }

  async request(path, options = {}) {
    const response = await this.fetch(`${this.apiUrl}${path}`, {
      ...options,
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: `Bearer ${this.token}`,
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'memory-docs-archive',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    });

    if (!response.ok) throw await this.createError(response);
    if (response.status === 204) return null;

    const text = await response.text();
    return text ? JSON.parse(text) : null;
  }

  async createError(response) {
    const body = await response.text();
    let detail = '';

    try {
      detail = JSON.parse(body).message || '';
    } catch {
      detail = body.slice(0, 180);
    }

    const error = new Error(`GitHub returned ${response.status}${detail ? `: ${detail}` : ''}`);
    error.status = response.status;
    error.code = 'GITHUB_ERROR';
    return error;
  }

  async listFiles() {
    let items;

    try {
      items = await this.request(this.contentApiPath('uploads'));
    } catch (error) {
      if (error.status !== 404) throw error;

      // A new repository has no uploads folder yet. Check the repository itself
      // so a misspelled repository name is not silently presented as an empty archive.
      await this.request(this.repositoryApiPath);
      return [];
    }

    if (!Array.isArray(items)) return [];
    return items
      .map(toPublicFile)
      .filter(Boolean)
      .sort((a, b) => b.uploadedAt.localeCompare(a.uploadedAt));
  }

  async uploadFile(path, buffer, originalName) {
    const result = await this.request(this.contentApiPath(path, false), {
      method: 'PUT',
      body: JSON.stringify({
        message: `chore: archive ${originalName}`,
        content: buffer.toString('base64'),
        branch: this.branch,
      }),
    });

    const file = toPublicFile({
      ...result.content,
      size: result.content.size ?? buffer.length,
    });

    return {
      ...file,
      commitUrl: result.commit?.html_url || null,
    };
  }

  async downloadFile(path) {
    const response = await this.fetch(`${this.apiUrl}${this.contentApiPath(path)}`, {
      headers: {
        Accept: 'application/vnd.github.raw+json',
        Authorization: `Bearer ${this.token}`,
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'memory-docs-archive',
      },
    });

    if (!response.ok) throw await this.createError(response);

    // The raw media type normally returns bytes directly. Handle a JSON content
    // response as well for compatibility with GitHub Enterprise installations.
    if (response.headers.get('content-type')?.includes('application/json')) {
      const data = await response.json();
      if (data.content) return Buffer.from(data.content, 'base64');

      const error = new Error('GitHub did not return downloadable file content.');
      error.status = 502;
      error.code = 'GITHUB_ERROR';
      throw error;
    }

    return Buffer.from(await response.arrayBuffer());
  }

  async deleteFile(path, sha, originalName) {
    await this.request(this.contentApiPath(path, false), {
      method: 'DELETE',
      body: JSON.stringify({
        message: `chore: remove archived ${originalName}`,
        branch: this.branch,
        sha,
      }),
    });
  }

  async upsertTextFile(path, content, message) {
    let sha;
    try {
      const existing = await this.request(this.contentApiPath(path));
      sha = existing.sha;
    } catch (error) {
      if (error.status !== 404) throw error;
    }

    return this.request(this.contentApiPath(path, false), {
      method: 'PUT',
      body: JSON.stringify({
        message,
        content: Buffer.from(content, 'utf8').toString('base64'),
        branch: this.branch,
        ...(sha ? { sha } : {}),
      }),
    });
  }

  async deleteDraftRelease(releaseId) {
    try {
      const release = await this.request(`${this.repositoryApiPath}/releases/${releaseId}`);
      if (!release.draft) return false;
      await this.deleteRelease(releaseId);
      return true;
    } catch (error) {
      // An already deleted draft needs no further cleanup.
      if (error.status === 404) return true;
      throw error;
    }
  }

  async assertReleaseUploadsAvailable() {
    try {
      // Any HTTP response proves that the host is reachable, including 404.
      await this.fetch(this.uploadUrl, { method: 'HEAD' });
    } catch (cause) {
      const error = new Error('The GitHub release upload host is unreachable.', { cause });
      error.code = 'RELEASE_UPLOAD_UNAVAILABLE';
      throw error;
    }
  }

  async createDraftRelease(metadata, tag) {
    return this.request(`${this.repositoryApiPath}/releases`, {
      method: 'POST',
      body: JSON.stringify({
        tag_name: tag,
        target_commitish: this.branch,
        name: metadata.originalName,
        body: serializeReleaseMetadata(metadata),
        draft: true,
      }),
    });
  }

  async uploadReleaseAsset(uploadUrl, part, body) {
    const separator = uploadUrl.includes('?') ? '&' : '?';
    const response = await this.fetch(`${uploadUrl}${separator}name=${encodeURIComponent(part.name)}`, {
      method: 'POST',
      headers: {
        Accept: 'application/vnd.github+json',
        Authorization: `Bearer ${this.token}`,
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'memory-docs-archive',
        'Content-Type': 'application/octet-stream',
        'Content-Length': String(part.size),
      },
      body,
      duplex: 'half',
    });

    if (!response.ok) throw await this.createError(response);
    return response.json();
  }

  async publishRelease(releaseId) {
    const release = await this.request(`${this.repositoryApiPath}/releases/${releaseId}`, {
      method: 'PATCH',
      body: JSON.stringify({ draft: false }),
    });
    const archive = toReleaseArchive(release);

    if (!archive) {
      const error = new Error('The published release is incomplete or has invalid metadata.');
      error.code = 'INCOMPLETE_RELEASE';
      throw error;
    }
    return archive;
  }

  async listReleaseArchives() {
    const releases = await this.request(`${this.repositoryApiPath}/releases?per_page=100`);
    if (!Array.isArray(releases)) return [];
    return releases.map(toReleaseArchive).filter(Boolean);
  }

  async getReleaseArchive(releaseId) {
    const release = await this.request(`${this.repositoryApiPath}/releases/${releaseId}`);
    return toReleaseArchive(release);
  }

  async deleteRelease(releaseId) {
    await this.request(`${this.repositoryApiPath}/releases/${releaseId}`, { method: 'DELETE' });
  }

  async deleteReleaseArchive(releaseId) {
    const release = await this.request(`${this.repositoryApiPath}/releases/${releaseId}`);
    const archive = toReleaseArchive(release);
    if (!archive) return false;

    await this.deleteRelease(releaseId);
    if (archive.tag.startsWith(RELEASE_TAG_PREFIX)) {
      try {
        await this.request(`${this.repositoryApiPath}/git/refs/tags/${encodeURIComponent(archive.tag)}`, {
          method: 'DELETE',
        });
      } catch (error) {
        // The release and assets are already gone; an orphaned tag is harmless.
        console.warn(`Could not remove archive tag ${archive.tag}: ${error.message}`);
      }
    }
    return true;
  }

  async downloadReleaseAsset(assetId) {
    const response = await this.fetch(`${this.apiUrl}${this.repositoryApiPath}/releases/assets/${assetId}`, {
      headers: {
        Accept: 'application/octet-stream',
        Authorization: `Bearer ${this.token}`,
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'memory-docs-archive',
      },
    });

    if (!response.ok) throw await this.createError(response);
    if (!response.body) throw new Error('GitHub returned an empty release asset response.');
    return response;
  }

  async uploadRepositoryPart(path, buffer, originalName) {
    const body = JSON.stringify({
      message: `chore: add part of ${originalName}`,
      content: buffer.toString('base64'),
      branch: this.branch,
    });

    // Rule scans and GitHub gateways can fail transiently. Retry the unique
    // part path, and after an ambiguous gateway/network error check whether
    // GitHub actually committed it before sending the bytes again.
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        const result = await this.request(this.contentApiPath(path, false), {
          method: 'PUT',
          body,
        });
        return result.content;
      } catch (error) {
        const ruleTimeout = error.status === 409 && /timed out validating the rule/i.test(error.message);
        const transientStatus = [408, 429, 500, 502, 503, 504].includes(error.status);
        const networkFailure = !error.status && (
          error.message === 'fetch failed'
          || ['ECONNRESET', 'ETIMEDOUT', 'EAI_AGAIN', 'UND_ERR_SOCKET'].includes(error.code)
        );
        const retryable = ruleTimeout || transientStatus || networkFailure;

        if (retryable && (networkFailure || error.status >= 500)) {
          try {
            const existing = await this.request(this.contentApiPath(path));
            if (existing?.type === 'file' && existing.size === buffer.length) return existing;
          } catch {
            // Preserve the original upload error if the existence check fails.
          }
        }

        if (!retryable || attempt === 3) throw error;
        await new Promise((resolve) => setTimeout(resolve, this.retryDelayMs * attempt));
      }
    }

    return null;
  }

  async listChunkedDirectory(directory = '') {
    const path = directory ? `${CHUNKED_ROOT}/${directory}` : CHUNKED_ROOT;
    try {
      const items = await this.request(this.contentApiPath(path));
      return Array.isArray(items) ? items : [];
    } catch (error) {
      if (error.status === 404) return [];
      throw error;
    }
  }

  async readTextFile(path) {
    const contents = await this.downloadFile(path);
    return contents.toString('utf8');
  }

  async getChunkedArchive(tag) {
    if (!new RegExp(`^${CHUNKED_TAG_PREFIX}\\d{13}-[a-f0-9]{8}$`).test(tag || '')) return null;

    let response;
    try {
      response = await this.request(this.contentApiPath(`${CHUNKED_ROOT}/${tag}/manifest.json`));
    } catch (error) {
      if (error.status === 404) return null;
      throw error;
    }

    const metadata = parseChunkedManifest(Buffer.from(response.content || '', 'base64').toString('utf8'));
    const branchPath = this.branch.split('/').map(encodeURIComponent).join('/');
    return toChunkedArchive(
      tag,
      metadata,
      `${this.repositoryUrl}/tree/${branchPath}/${CHUNKED_ROOT}/${tag}`,
    );
  }

  async listChunkedArchives() {
    let items;
    try {
      items = await this.request(this.contentApiPath(CHUNKED_ROOT));
    } catch (error) {
      if (error.status === 404) return [];
      throw error;
    }

    const archives = [];
    for (const item of Array.isArray(items) ? items : []) {
      if (item.type !== 'dir' || !item.name?.startsWith(CHUNKED_TAG_PREFIX)) continue;
      const archive = await this.getChunkedArchive(item.name);
      if (archive) archives.push(archive);
    }
    return archives;
  }

  async deletePaths(paths, message) {
    if (!paths.length) return;
    const branchPath = this.branch.split('/').map(encodeURIComponent).join('/');
    const reference = await this.request(`${this.repositoryApiPath}/git/ref/heads/${branchPath}`);
    const parentSha = reference.object.sha;
    const parent = await this.request(`${this.repositoryApiPath}/git/commits/${parentSha}`);
    const tree = await this.request(`${this.repositoryApiPath}/git/trees`, {
      method: 'POST',
      body: JSON.stringify({
        base_tree: parent.tree.sha,
        tree: paths.map((path) => ({ path, mode: '100644', type: 'blob', sha: null })),
      }),
    });
    const commit = await this.request(`${this.repositoryApiPath}/git/commits`, {
      method: 'POST',
      body: JSON.stringify({ message, tree: tree.sha, parents: [parentSha] }),
    });
    await this.request(`${this.repositoryApiPath}/git/refs/heads/${branchPath}`, {
      method: 'PATCH',
      body: JSON.stringify({ sha: commit.sha, force: false }),
    });
  }

  async deleteChunkedArchive(tag) {
    const archive = await this.getChunkedArchive(tag);
    if (!archive) return null;
    await this.deletePaths(
      [...archive.parts.map((part) => part.path), `${archive.path}/manifest.json`],
      `chore: remove chunked archive ${archive.name}`,
    );
    return archive;
  }
}
