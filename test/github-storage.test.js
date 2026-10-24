import test from 'node:test';
import assert from 'node:assert/strict';
import { GitHubStorage } from '../lib/github-storage.js';

const settings = {
  token: 'test-token',
  owner: 'example',
  repo: 'archive',
  branch: 'main',
};

const storedPath = 'uploads/1761301800000-deadbeef-docs.zip';

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

test('uploadFile sends base64 content and the target branch to GitHub', async () => {
  let requestUrl;
  let requestOptions;
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async (url, options) => {
      requestUrl = url;
      requestOptions = options;
      return jsonResponse({
        content: {
          type: 'file',
          path: storedPath,
          size: 3,
          sha: 'a'.repeat(40),
          html_url: 'https://github.com/example/archive/blob/main/file',
        },
        commit: { html_url: 'https://github.com/example/archive/commit/123' },
      }, 201);
    },
  });

  const file = await storage.uploadFile(storedPath, Buffer.from('zip'), 'docs.zip');
  const body = JSON.parse(requestOptions.body);

  assert.equal(requestUrl, `https://api.github.com/repos/example/archive/contents/${storedPath}`);
  assert.equal(requestOptions.method, 'PUT');
  assert.equal(requestOptions.headers.Authorization, 'Bearer test-token');
  assert.equal(body.content, Buffer.from('zip').toString('base64'));
  assert.equal(body.branch, 'main');
  assert.equal(file.name, 'docs.zip');
  assert.equal(file.size, 3);
  assert.equal(file.commitUrl, 'https://github.com/example/archive/commit/123');
});

test('repository parts retry transient repository-rule validation timeouts', async () => {
  let attempts = 0;
  const storage = new GitHubStorage({
    ...settings,
    retryDelayMs: 1,
    fetchImpl: async () => {
      attempts += 1;
      if (attempts < 3) {
        return jsonResponse({ message: 'Repository rule violations found\n\nTimed out validating the rule.' }, 409);
      }
      return jsonResponse({ content: { sha: 'd'.repeat(40), size: 4 } }, 201);
    },
  });

  const part = await storage.uploadRepositoryPart(
    'uploads/large/memory-docs-test/archive.part001',
    Buffer.from('part'),
    'archive.7z',
  );
  assert.equal(attempts, 3);
  assert.equal(part.size, 4);
});

test('repository parts retry temporary GitHub gateway failures', async () => {
  let putAttempts = 0;
  const storage = new GitHubStorage({
    ...settings,
    retryDelayMs: 1,
    fetchImpl: async (url, options) => {
      if (options.method === 'PUT') {
        putAttempts += 1;
        if (putAttempts === 1) return jsonResponse({ message: "We couldn't respond in time." }, 504);
        return jsonResponse({ content: { type: 'file', sha: 'e'.repeat(40), size: 4 } }, 201);
      }
      return jsonResponse({ message: 'Not Found' }, 404);
    },
  });

  const part = await storage.uploadRepositoryPart('uploads/large/test/part001', Buffer.from('part'), 'archive.7z');
  assert.equal(putAttempts, 2);
  assert.equal(part.size, 4);
});

test('a gateway timeout does not duplicate a part GitHub already stored', async () => {
  let putAttempts = 0;
  const storage = new GitHubStorage({
    ...settings,
    retryDelayMs: 1,
    fetchImpl: async (url, options) => {
      if (options.method === 'PUT') {
        putAttempts += 1;
        return jsonResponse({ message: "We couldn't respond in time." }, 504);
      }
      return jsonResponse({ type: 'file', sha: 'f'.repeat(40), size: 4 });
    },
  });

  const part = await storage.uploadRepositoryPart('uploads/large/test/part001', Buffer.from('part'), 'archive.7z');
  assert.equal(putAttempts, 1);
  assert.equal(part.sha, 'f'.repeat(40));
});

test('listFiles maps and sorts archive entries from newest to oldest', async () => {
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => jsonResponse([
      { type: 'file', path: 'uploads/1761301800000-deadbeef-old.zip', size: 10, sha: 'a'.repeat(40) },
      { type: 'file', path: 'uploads/README.md', size: 20, sha: 'b'.repeat(40) },
      { type: 'file', path: 'uploads/1761390000000-1234abcd-new.7z', size: 30, sha: 'c'.repeat(40) },
    ]),
  });

  const files = await storage.listFiles();
  assert.deepEqual(files.map((file) => file.name), ['new.7z', 'old.zip']);
});

test('a missing uploads directory is empty only when the repository exists', async () => {
  let calls = 0;
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => {
      calls += 1;
      return calls === 1
        ? jsonResponse({ message: 'Not Found' }, 404)
        : jsonResponse({ full_name: 'example/archive' });
    },
  });

  assert.deepEqual(await storage.listFiles(), []);
  assert.equal(calls, 2);
});

test('GitHub errors retain their status for a safe API response', async () => {
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => jsonResponse({ message: 'Bad credentials' }, 401),
  });

  await assert.rejects(
    storage.listFiles(),
    (error) => error.code === 'GITHUB_ERROR' && error.status === 401,
  );
});

test('downloadFile accepts raw and JSON content responses', async () => {
  const rawStorage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => new Response(Buffer.from('raw zip'), {
      headers: { 'Content-Type': 'application/octet-stream' },
    }),
  });
  assert.equal((await rawStorage.downloadFile(storedPath)).toString(), 'raw zip');

  const jsonStorage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => jsonResponse({ content: Buffer.from('json zip').toString('base64') }),
  });
  assert.equal((await jsonStorage.downloadFile(storedPath)).toString(), 'json zip');
});
