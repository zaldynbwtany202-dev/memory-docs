import test from 'node:test';
import assert from 'node:assert/strict';
import {
  createReleasePlan,
  parseReleaseMetadata,
  RELEASE_PART_SIZE,
  serializeReleaseMetadata,
  toPublicReleaseArchive,
  toReleaseArchive,
} from '../lib/release-archive.js';

const fixedOptions = { timestamp: 1761301800000, uploadId: '12345678-abcd-4abc-9abc-123456789012' };

test('a 7 GiB archive becomes exactly four release parts', () => {
  const size = 7 * 1024 ** 3;
  const plan = createReleasePlan('huge-backup.7z', size, fixedOptions);

  assert.equal(plan.parts.length, 4);
  assert.equal(plan.metadata.originalName, 'huge-backup.7z');
  assert.equal(plan.metadata.size, size);
  assert.equal(plan.metadata.parts.length, 4);
  assert.ok(RELEASE_PART_SIZE < 2 * 1024 ** 3);
  assert.equal(plan.parts.reduce((sum, part) => sum + part.size, 0), size);
  assert.deepEqual(plan.parts.map((part) => part.size), [
    RELEASE_PART_SIZE,
    RELEASE_PART_SIZE,
    RELEASE_PART_SIZE,
    RELEASE_PART_SIZE,
  ]);
  assert.deepEqual(plan.parts.map((part) => part.name), [
    `${plan.tag}.part001`,
    `${plan.tag}.part002`,
    `${plan.tag}.part003`,
    `${plan.tag}.part004`,
  ]);
});

test('a 7 billion-byte archive also uses four parts with a smaller final part', () => {
  const plan = createReleasePlan('backup.7z', 7_000_000_000, fixedOptions);
  assert.equal(plan.parts.length, 4);
  assert.equal(plan.parts.at(-1).size, 7_000_000_000 - (3 * RELEASE_PART_SIZE));
  assert.ok(plan.parts.at(-1).size > 0);
  assert.ok(plan.parts.at(-1).size < RELEASE_PART_SIZE);
});

test('release metadata round-trips and rejects unrelated releases', () => {
  const plan = createReleasePlan('backup.7z', 7 * 1024 ** 3, fixedOptions);
  const body = serializeReleaseMetadata(plan.metadata);
  assert.deepEqual(parseReleaseMetadata(body), plan.metadata);
  assert.equal(parseReleaseMetadata('An ordinary release'), null);
  assert.equal(parseReleaseMetadata('<!-- memory-docs-archive\n{"version":2}\n-->'), null);
});

function releaseFixture() {
  const size = 2 * RELEASE_PART_SIZE;
  const plan = createReleasePlan('backup.7z', size, fixedOptions);
  return {
    plan,
    release: {
      id: 987654,
      tag_name: plan.tag,
      draft: false,
      body: serializeReleaseMetadata(plan.metadata),
      created_at: plan.metadata.uploadedAt,
      html_url: 'https://github.com/example/archive/releases/tag/example',
      assets: plan.parts.map((part, index) => ({
        id: 5000 + index,
        name: part.name,
        size: part.size,
        state: 'uploaded',
      })),
    },
  };
}

test('published releases map to one downloadable archive with ordered assets', () => {
  const { release } = releaseFixture();
  const archive = toReleaseArchive(release);

  assert.equal(archive.kind, 'release');
  assert.equal(archive.releaseId, '987654');
  assert.equal(archive.name, 'backup.7z');
  assert.equal(archive.partCount, 2);
  assert.equal(archive.assets.length, 2);
  assert.equal(archive.downloadUrl, '/api/large-files/987654/download');

  const publicArchive = toPublicReleaseArchive(archive);
  assert.equal(publicArchive.assets, undefined);
  assert.equal(publicArchive.tag, undefined);
  assert.equal(publicArchive.partCount, 2);
});

test('drafts and releases with missing parts stay hidden', () => {
  const { release } = releaseFixture();
  assert.equal(toReleaseArchive({ ...release, draft: true }), null);
  assert.equal(toReleaseArchive({ ...release, assets: release.assets.slice(1) }), null);
  assert.equal(toReleaseArchive({ ...release, body: 'Not an archive' }), null);
});
