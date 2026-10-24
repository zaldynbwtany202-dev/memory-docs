import test from 'node:test';
import assert from 'node:assert/strict';
import { CHUNKED_PART_SIZE, createChunkedPlan } from '../lib/chunked-archive.js';
import { parseChunkedUploadStatus, recoverChunkedSession } from '../lib/chunked-recovery.js';
import { buildUploadStatusText } from '../lib/upload-status.js';

const options = { timestamp: 1761301800000, uploadId: '12345678-abcd-4abc-9abc-123456789012' };

function sessionWithStatus(status = 'IN_PROGRESS') {
  const plan = createChunkedPlan('New folder.7z', (2 * CHUNKED_PART_SIZE) + 123, options);
  const session = {
    ...plan,
    strategy: 'chunked',
    releaseId: null,
    statusPath: `uploads/status/${plan.tag}.txt`,
    uploaded: new Map([[0, { index: 0 }]]),
  };
  return { plan, text: buildUploadStatusText(session, status) };
}

test('an interrupted repository upload recovers its exact plan and stored parts', () => {
  const { plan, text } = sessionWithStatus();
  const parsed = parseChunkedUploadStatus(text);
  assert.equal(parsed.tag, plan.tag);
  assert.equal(parsed.uploadId, plan.uploadId);
  assert.deepEqual(parsed.parts, plan.parts);

  const remoteItems = plan.parts.slice(0, 2).map((part) => ({
    type: 'file',
    path: part.path,
    size: part.size,
    sha: `${part.index}`.repeat(40),
  }));
  const recovered = recoverChunkedSession(parsed, remoteItems);
  assert.deepEqual([...recovered.uploaded.keys()], [0, 1]);
  assert.equal(recovered.uploaded.get(1).size, CHUNKED_PART_SIZE);
  assert.equal(recovered.statusPath, `uploads/status/${plan.tag}.txt`);
});

test('cancelled or incomplete status records are not resumed', () => {
  assert.equal(parseChunkedUploadStatus(sessionWithStatus('CANCELLED').text), null);
  assert.equal(parseChunkedUploadStatus(sessionWithStatus('INCOMPLETE').text), null);
});

test('recovery rejects a stored part whose size differs from the plan', () => {
  const { plan, text } = sessionWithStatus();
  const parsed = parseChunkedUploadStatus(text);
  assert.throws(
    () => recoverChunkedSession(parsed, [{
      type: 'file',
      path: plan.parts[0].path,
      size: 12,
      sha: 'a'.repeat(40),
    }]),
    (error) => error.code === 'INCOMPLETE_RELEASE',
  );
});
