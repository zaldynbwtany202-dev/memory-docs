import { toPublicFile } from './file-utils.js';

export class GitHubStorage {
  constructor({ token, owner, repo, branch = 'main', apiUrl = 'https://api.github.com', fetchImpl = fetch }) {
    this.token = token;
    this.owner = owner;
    this.repo = repo;
    this.branch = branch;
    this.apiUrl = apiUrl.replace(/\/$/, '');
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
        'User-Agent': 'memory-docs-zip-archive',
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
        'User-Agent': 'memory-docs-zip-archive',
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
}
