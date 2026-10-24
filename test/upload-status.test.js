import test from 'node:test';
import assert from 'node:assert/strict';
import { buildUploadStatusText } from '../lib/upload-status.js';
import { GitHubStorage } from '../lib/github-storage.js';

function sessionFixture() {
  const tag = 'memory-docs-status-test';
  return {
    uploadId: 'upload-123',
    releaseId: '55',
    tag,
    statusPath: `uploads/status/${tag}.txt`,
    metadata: { originalName: 'نسخة كبيرة.7z', size: 7 * 1024 ** 3 },
    parts: Array.from({ length: 4 }, (_, index) => ({
      index,
      name: `${tag}.part00${index + 1}`,
      size: 100,
    })),
    uploaded: new Map([
      [0, { id: '1' }],
      [1, { id: '2' }],
    ]),
  };
}

test('an in-progress status clearly counts received and remaining parts', () => {
  const text = buildUploadStatusText(
    sessionFixture(),
    'IN_PROGRESS',
    'اختبار',
    new Date('2026-10-24T12:00:00Z'),
  );

  assert.match(text, /STATUS_CODE: IN_PROGRESS/);
  assert.match(text, /اسم الملف: نسخة كبيرة\.7z/);
  assert.match(text, /العدد الكلي: 4/);
  assert.match(text, /الأجزاء التي وصلت: 2/);
  assert.match(text, /الأجزاء المتبقية: 2/);
  assert.match(text, /\[وصل\].*part001/);
  assert.match(text, /\[لم يصل\].*part003/);
  assert.match(text, /لا تعتبر هذا أرشيفًا مكتملًا/);
});

test('complete is the only status that describes a usable archive', () => {
  const session = sessionFixture();
  session.uploaded.set(2, { id: '3' });
  session.uploaded.set(3, { id: '4' });
  const text = buildUploadStatusText(session, 'COMPLETE');

  assert.match(text, /STATUS_CODE: COMPLETE/);
  assert.match(text, /الأجزاء المتبقية: 0/);
  assert.match(text, /الأرشيف مكتمل/);
});

test('status text files are sent to GitHub as UTF-8 base64', async () => {
  let putBody;
  const storage = new GitHubStorage({
    token: 'test', owner: 'example', repo: 'archive', branch: 'main',
    fetchImpl: async (url, options) => {
      if (options.method === 'PUT') {
        putBody = JSON.parse(options.body);
        return new Response(JSON.stringify({ content: {} }), { status: 201 });
      }
      return new Response(JSON.stringify({ message: 'Not Found' }), { status: 404 });
    },
  });

  await storage.upsertTextFile('uploads/status/test.txt', 'الحالة: غير مكتمل', 'update status');
  assert.equal(Buffer.from(putBody.content, 'base64').toString('utf8'), 'الحالة: غير مكتمل');
  assert.equal(putBody.branch, 'main');
  assert.equal(putBody.sha, undefined);
});
