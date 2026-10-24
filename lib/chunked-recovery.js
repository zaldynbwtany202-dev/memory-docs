import { CHUNKED_TAG_PREFIX, createChunkedPlan } from './chunked-archive.js';

function statusField(text, label) {
  return text.match(new RegExp(`^${label}:\\s*(.+)$`, 'm'))?.[1]?.trim() || '';
}

export function parseChunkedUploadStatus(text) {
  if (typeof text !== 'string' || !/^STATUS_CODE: IN_PROGRESS$/m.test(text)) return null;
  if (!/^طريقة التخزين: .*uploads\/large/m.test(text)) return null;

  const originalName = statusField(text, 'اسم الملف');
  const size = Number(statusField(text, 'الحجم الكلي بالبايت'));
  const uploadId = statusField(text, 'معرّف العملية');
  const tag = statusField(text, 'وسم الأرشيف');
  const tagMatch = tag.match(/^memory-docs-(\d{13})-[a-f0-9]{8}$/);
  const uuidPattern = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;

  if (!originalName || !Number.isSafeInteger(size) || size <= 0 || !tagMatch || !uuidPattern.test(uploadId)) {
    return null;
  }

  const plan = createChunkedPlan(originalName, size, {
    uploadId,
    timestamp: Number(tagMatch[1]),
  });
  if (plan.tag !== tag || !tag.startsWith(CHUNKED_TAG_PREFIX)) return null;
  return plan;
}

export function recoverChunkedSession(plan, remoteItems) {
  const itemsByPath = new Map(
    remoteItems.filter((item) => item.type === 'file').map((item) => [item.path, item]),
  );
  const uploaded = new Map();

  for (const part of plan.parts) {
    const item = itemsByPath.get(part.path);
    if (!item) continue;
    if (item.size !== part.size) {
      const error = new Error(`Stored part size does not match its upload plan: ${part.path}`);
      error.code = 'INCOMPLETE_RELEASE';
      throw error;
    }
    uploaded.set(part.index, {
      index: part.index,
      id: String(item.sha),
      name: part.name,
      path: part.path,
      size: part.size,
    });
  }

  return {
    ...plan,
    strategy: 'chunked',
    releaseId: null,
    releaseUrl: null,
    statusPath: `uploads/status/${plan.tag}.txt`,
    uploaded,
    updatedAt: Date.now(),
  };
}
