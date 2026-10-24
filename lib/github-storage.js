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
  }) {
    this.token = token;
    this.owner = owner;
    this.repo = repo;
    this.branch = branch;
    this.apiUrl = apiUrl.replace(/\/$/, '');
    this.uploadUrl = uploadUrl.replace(/\/$/, '');
    this.fetch = fetchImpl;
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
}
