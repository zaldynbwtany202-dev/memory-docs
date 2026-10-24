import test from 'node:test';
import assert from 'node:assert/strict';
import {
  CHUNKED_PART_SIZE,
  createChunkedPlan,
  parseChunkedManifest,
  toChunkedArchive,
  toPublicChunkedArchive,
} from '../lib/chunked-archive.js';
import { REPOSITORY_FILE_SIZE_LIMIT } from '../lib/release-archive.js';

const options = { timestamp: 1761301800000, uploadId: '12345678-abcd-4abc-9abc-123456789012' };

test('the repository fallback splits 7 GiB into 448 validation-safe parts', () => {
  const size = 7 * 1024 ** 3;
  const plan = createChunkedPlan('huge.7z', size, options);

  assert.equal(plan.parts.length, 448);
  assert.equal(plan.parts.reduce((sum, part) => sum + part.size, 0), size);
  assert.ok(plan.parts.every((part) => part.size <= CHUNKED_PART_SIZE));
  assert.ok(CHUNKED_PART_SIZE < REPOSITORY_FILE_SIZE_LIMIT);
  assert.equal(plan.parts[0].path, `${plan.directory}/${plan.parts[0].name}`);
  assert.equal(plan.manifestPath, `${plan.directory}/manifest.json`);
  assert.equal(plan.metadata.parts.length, 448);
});

test('chunked manifests describe one downloadable original archive', () => {
  const plan = createChunkedPlan('huge.7z', 2 * CHUNKED_PART_SIZE, options);
  const parsed = parseChunkedManifest(JSON.stringify(plan.metadata));
  const archive = toChunkedArchive(plan.tag, parsed, 'https://github.com/example/archive/tree/main/uploads/large');

  assert.deepEqual(parsed, plan.metadata);
  assert.equal(archive.kind, 'chunked');
  assert.equal(archive.name, 'huge.7z');
  assert.equal(archive.partCount, 2);
  assert.match(archive.downloadUrl, /^\/api\/chunked-files\//);
  assert.equal(toPublicChunkedArchive(archive).parts, undefined);
});

test('invalid manifests and traversal paths are rejected', () => {
  const plan = createChunkedPlan('huge.7z', CHUNKED_PART_SIZE, options);
  assert.equal(parseChunkedManifest({}), null);
  assert.equal(parseChunkedManifest({
    ...plan.metadata,
    parts: [{ ...plan.metadata.parts[0], path: '../secret' }],
  }), null);
  assert.equal(toChunkedArchive('../bad', plan.metadata), null);
});
