import test from 'node:test';
import assert from 'node:assert/strict';
import {
  buildStoragePath,
  decodeUploadName,
  getArchiveExtension,
  getArchiveType,
  isValidStoragePath,
  parseStoragePath,
  sanitizeFilename,
  toPublicFile,
} from '../lib/file-utils.js';

test('sanitizeFilename removes paths and preserves supported extensions', () => {
  assert.equal(sanitizeFilename('../../documents/Project.ZIP'), 'Project.zip');
  assert.equal(sanitizeFilename('..\\..\\backup.7Z'), 'backup.7z');
  assert.equal(sanitizeFilename('  my   archive.zip  '), 'my archive.zip');
  assert.equal(sanitizeFilename(''), 'archive.zip');
  assert.equal(getArchiveExtension('BACKUP.7Z'), '.7z');
  assert.equal(getArchiveExtension('backup.rar'), null);
});

test('UTF-8 names, including Arabic names, survive multipart decoding', () => {
  const arabicName = 'نسخة المشروع.7z';
  const mojibake = Buffer.from(arabicName, 'utf8').toString('latin1');
  assert.equal(decodeUploadName(mojibake), arabicName);
  assert.equal(sanitizeFilename(mojibake), arabicName);
});

test('storage paths round-trip the original name and upload date', () => {
  const timestamp = Date.UTC(2026, 9, 24, 12, 30);
  const path = buildStoragePath('project backup.7z', { timestamp, suffix: 'deadbeef' });
  assert.equal(path, `uploads/${timestamp}-deadbeef-project backup.7z`);
  assert.deepEqual(parseStoragePath(path), {
    uploadedAt: new Date(timestamp).toISOString(),
    originalName: 'project backup.7z',
  });
  assert.equal(isValidStoragePath(path), true);
});

test('storage validation rejects paths not created by the archive', () => {
  assert.equal(isValidStoragePath('uploads/manual.7z'), false);
  assert.equal(isValidStoragePath('../secrets.zip'), false);
  assert.equal(isValidStoragePath('uploads/1761301800000-not-a-suffix-file.zip'), false);
  assert.equal(isValidStoragePath(null), false);

  const validZip = buildStoragePath('version..final.zip', { timestamp: 1761301800000, suffix: '1234abcd' });
  const validSevenZip = buildStoragePath('version.final.7z', { timestamp: 1761301800000, suffix: '1234abcd' });
  assert.equal(isValidStoragePath(validZip), true);
  assert.equal(isValidStoragePath(validSevenZip), true);
});

test('ZIP and 7z signatures are checked instead of trusting the extension', () => {
  assert.equal(getArchiveType(Buffer.from([0x50, 0x4b, 0x03, 0x04, 0x00])), 'zip');
  assert.equal(getArchiveType(Buffer.from([0x50, 0x4b, 0x05, 0x06, 0x00])), 'zip');
  assert.equal(getArchiveType(Buffer.from([0x50, 0x4b, 0x07, 0x08, 0x00])), 'zip');
  assert.equal(getArchiveType(Buffer.from([0x37, 0x7a, 0xbc, 0xaf, 0x27, 0x1c, 0x00])), '7z');
  assert.equal(getArchiveType(Buffer.from([0x37, 0x7a, 0xbc, 0xaf, 0x27])), null);
  assert.equal(getArchiveType(Buffer.from('not an archive')), null);
  assert.equal(getArchiveType(Buffer.from('PK')), null);
});

test('public file metadata supports 7z and ignores unrelated repository contents', () => {
  const path = buildStoragePath('docs.7z', { timestamp: 1761301800000, suffix: '1234abcd' });
  const file = toPublicFile({
    type: 'file',
    path,
    size: 1234,
    sha: 'a'.repeat(40),
    html_url: 'https://github.com/example/repo/blob/main/file',
  });

  assert.equal(file.name, 'docs.7z');
  assert.equal(file.size, 1234);
  assert.match(file.downloadUrl, /^\/api\/files\/download\?path=/);
  assert.equal(toPublicFile({ type: 'file', path: 'uploads/README.md' }), null);
  assert.equal(toPublicFile({ type: 'dir', path }), null);
});
