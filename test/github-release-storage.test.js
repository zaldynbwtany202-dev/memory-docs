import test from 'node:test';
import assert from 'node:assert/strict';
import { Readable } from 'node:stream';
import { GitHubStorage } from '../lib/github-storage.js';

const settings = { token: 'test-token', owner: 'example', repo: 'archive', branch: 'main' };

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

test('release upload preflight reports an unreachable host before creating a draft', async () => {
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async () => {
      throw new TypeError('fetch failed');
    },
  });

  await assert.rejects(
    storage.assertReleaseUploadsAvailable(),
    (error) => error.code === 'RELEASE_UPLOAD_UNAVAILABLE',
  );
});

test('release assets upload as raw streams with their exact byte length', async () => {
  let uploadRequest;
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async (url, options) => {
      uploadRequest = { url, options };
      const received = await new Response(options.body).arrayBuffer();
      assert.equal(received.byteLength, 9);
      return jsonResponse({ id: 123, name: 'archive.part001', size: 9 }, 201);
    },
  });
  const part = { name: 'archive.part001', size: 9 };
  const stream = Readable.toWeb(Readable.from([Buffer.from('part-data')]));
  const asset = await storage.uploadReleaseAsset(
    'https://uploads.github.com/repos/example/archive/releases/55/assets',
    part,
    stream,
  );

  assert.equal(asset.id, 123);
  assert.match(uploadRequest.url, /\?name=archive\.part001$/);
  assert.equal(uploadRequest.options.headers['Content-Type'], 'application/octet-stream');
  assert.equal(uploadRequest.options.headers['Content-Length'], '9');
  assert.equal(uploadRequest.options.duplex, 'half');
});

test('draft release creation includes the hidden archive metadata', async () => {
  let requestBody;
  const storage = new GitHubStorage({
    ...settings,
    fetchImpl: async (url, options) => {
      requestBody = JSON.parse(options.body);
      return jsonResponse({ id: 55, upload_url: 'https://uploads.github.com/release/55/assets{?name}' }, 201);
    },
  });
  const metadata = { originalName: 'backup.7z' };
  const release = await storage.createDraftRelease(metadata, 'memory-docs-test');

  assert.equal(release.id, 55);
  assert.equal(requestBody.tag_name, 'memory-docs-test');
  assert.equal(requestBody.target_commitish, 'main');
  assert.equal(requestBody.draft, true);
  assert.match(requestBody.body, /memory-docs-archive/);
});
