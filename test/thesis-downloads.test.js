import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { app } from '../server.js';

async function startTestServer(t) {
  const server = app.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  }));
  return `http://127.0.0.1:${server.address().port}`;
}

function sha256(contents) {
  return createHash('sha256').update(contents).digest('hex');
}

test('thesis page exposes working PDF and DOCX download links', async (t) => {
  const baseUrl = await startTestServer(t);
  const redirect = await fetch(`${baseUrl}/thesis`, { redirect: 'manual' });
  assert.equal(redirect.status, 302);
  assert.equal(redirect.headers.get('location'), '/thesis.html');

  const response = await fetch(`${baseUrl}/thesis.html`);
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /href="\/thesis\/download\/pdf"/);
  assert.match(html, /href="\/thesis\/download\/docx"/);
  assert.doesNotMatch(html, /sandbox:|localhost|127\.0\.0\.1/);
});

test('thesis download routes return the exact audited deliverables', async (t) => {
  const baseUrl = await startTestServer(t);
  const documents = [
    ['pdf', 'application/pdf'],
    ['docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
  ];

  for (const [format, mimeType] of documents) {
    const fileName = `These_revisee_BERKANE_Dhiyaddine.${format}`;
    const fileUrl = new URL(`../thesis_revision/deliverables/${fileName}`, import.meta.url);
    const expected = await readFile(fileURLToPath(fileUrl));
    const response = await fetch(`${baseUrl}/thesis/download/${format}`);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('content-type'), mimeType);
    assert.match(response.headers.get('content-disposition'), /^attachment;/);
    assert.match(response.headers.get('content-disposition'), new RegExp(fileName));
    assert.equal(Number(response.headers.get('content-length')), expected.length);
    const contents = Buffer.from(await response.arrayBuffer());
    assert.equal(sha256(contents), sha256(expected));
  }
});

test('unknown thesis download formats return 404', async (t) => {
  const baseUrl = await startTestServer(t);
  const response = await fetch(`${baseUrl}/thesis/download/pptx`);
  assert.equal(response.status, 404);
});
