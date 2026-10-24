import test from 'node:test';
import assert from 'node:assert/strict';
import {
  buildStoragePath,
  decodeUploadName,
  isValidStoragePath,
  isZipBuffer,
  parseStoragePath,
  sanitizeFilename,
  toPublicFile,
} from '../lib/file-utils.js';

test('sanitizeFilename removes paths and normalizes the ZIP extension', () => {
  assert.equal(sanitizeFilename('../../documents/Project.ZIP'), 'Project.zip');
  assert.equal(sanitizeFilename('..\\..\\backup.zip'), 'backup.zip');
  assert.equal(sanitizeFilename('  my   archive.zip  '), 'my archive.zip');
  assert.equal(sanitizeFilename(''), 'archive.zip');
});

test('UTF-8 names, including Arabic names, survive multipart decoding', () => {
  const arabicName = 'نسخة المشروع.zip';
  const mojibake = Buffer.from(arabicName, 'utf8').toString('latin1');
  assert.equal(decodeUploadName(mojibake), arabicName);
  assert.equal(sanitizeFilename(mojibake), arabicName);
});

test('storage paths round-trip the original name and upload date', () => {
  const timestamp = Date.UTC(2026, 9, 24, 12, 30);
  const path = buildStoragePath('project backup.zip', { timestamp, suffix: 'deadbeef' });
  assert.equal(path, `uploads/${timestamp}-deadbeef-project backup.zip`);
  assert.deepEqual(parseStoragePath(path), {
    uploadedAt: new Date(timestamp).toISOString(),
    originalName: 'project backup.zip',
  });
  assert.equal(isValidStoragePath(path), true);
});

test('storage validation rejects paths not created by the archive', () => {
  assert.equal(isValidStoragePath('uploads/manual.zip'), false);
  assert.equal(isValidStoragePath('../secrets.zip'), false);
  assert.equal(isValidStoragePath('uploads/1761301800000-not-a-suffix-file.zip'), false);
  assert.equal(isValidStoragePath(null), false);

  const validWithDots = buildStoragePath('version..final.zip', { timestamp: 1761301800000, suffix: '1234abcd' });
  assert.equal(isValidStoragePath(validWithDots), true);
});

test('ZIP signatures are checked instead of trusting the extension', () => {
  assert.equal(isZipBuffer(Buffer.from([0x50, 0x4b, 0x03, 0x04, 0x00])), true);
  assert.equal(isZipBuffer(Buffer.from([0x50, 0x4b, 0x05, 0x06, 0x00])), true);
  assert.equal(isZipBuffer(Buffer.from([0x50, 0x4b, 0x07, 0x08, 0x00])), true);
  assert.equal(isZipBuffer(Buffer.from('not a zip file')), false);
  assert.equal(isZipBuffer(Buffer.from('PK')), false);
});

test('public file metadata ignores unrelated repository contents', () => {
  const path = buildStoragePath('docs.zip', { timestamp: 1761301800000, suffix: '1234abcd' });
  const file = toPublicFile({
    type: 'file',
    path,
    size: 1234,
    sha: 'a'.repeat(40),
    html_url: 'https://github.com/example/repo/blob/main/file',
  });

  assert.equal(file.name, 'docs.zip');
  assert.equal(file.size, 1234);
  assert.match(file.downloadUrl, /^\/api\/files\/download\?path=/);
  assert.equal(toPublicFile({ type: 'file', path: 'uploads/README.md' }), null);
  assert.equal(toPublicFile({ type: 'dir', path }), null);
});
