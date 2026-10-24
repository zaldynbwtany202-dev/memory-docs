import { randomUUID } from 'node:crypto';

// Keep each Contents API request comfortably below GitHub's validation limits.
// Very large base64 payloads can time out during repository rule validation.
export const CHUNKED_PART_SIZE = 32 * 1024 * 1024;
export const CHUNKED_ROOT = 'uploads/large';
export const CHUNKED_TAG_PREFIX = 'memory-docs-';

export function createChunkedPlan(originalName, size, options = {}) {
  if (!Number.isSafeInteger(size) || size <= 0) throw new TypeError('Invalid archive size.');

  const uploadId = options.uploadId || randomUUID();
  const timestamp = options.timestamp || Date.now();
  const tag = `${CHUNKED_TAG_PREFIX}${timestamp}-${uploadId.slice(0, 8)}`;
  const directory = `${CHUNKED_ROOT}/${tag}`;
  const parts = Array.from({ length: Math.ceil(size / CHUNKED_PART_SIZE) }, (_, index) => {
    const name = `${tag}.part${String(index + 1).padStart(3, '0')}`;
    return {
      index,
      name,
      path: `${directory}/${name}`,
      size: Math.min(CHUNKED_PART_SIZE, size - (index * CHUNKED_PART_SIZE)),
    };
  });

  return {
    uploadId,
    tag,
    directory,
    manifestPath: `${directory}/manifest.json`,
    chunkSize: CHUNKED_PART_SIZE,
    parts,
    metadata: {
      version: 1,
      originalName,
      size,
      uploadedAt: new Date(timestamp).toISOString(),
      partSize: CHUNKED_PART_SIZE,
      parts: parts.map((part) => ({ name: part.name, path: part.path, size: part.size })),
    },
  };
}

export function parseChunkedManifest(value) {
  try {
    const metadata = typeof value === 'string' ? JSON.parse(value) : value;
    const valid = metadata?.version === 1
      && typeof metadata.originalName === 'string'
      && Number.isSafeInteger(metadata.size)
      && metadata.size > 0
      && Array.isArray(metadata.parts)
      && metadata.parts.length > 0
      && metadata.parts.every((part) => (
        typeof part.name === 'string'
        && typeof part.path === 'string'
        && part.path.startsWith(`${CHUNKED_ROOT}/${CHUNKED_TAG_PREFIX}`)
        && !part.path.includes('..')
        && Number.isSafeInteger(part.size)
        && part.size > 0
        && part.size <= CHUNKED_PART_SIZE
      ));
    if (!valid) return null;
    if (metadata.parts.reduce((sum, part) => sum + part.size, 0) !== metadata.size) return null;
    return metadata;
  } catch {
    return null;
  }
}

export function toChunkedArchive(tag, metadata, htmlUrl = null) {
  if (!tag?.startsWith(CHUNKED_TAG_PREFIX)) return null;
  const parsed = parseChunkedManifest(metadata);
  if (!parsed) return null;

  return {
    kind: 'chunked',
    tag,
    name: parsed.originalName,
    path: `${CHUNKED_ROOT}/${tag}`,
    size: parsed.size,
    uploadedAt: parsed.uploadedAt,
    htmlUrl,
    downloadUrl: `/api/chunked-files/${encodeURIComponent(tag)}/download`,
    partCount: parsed.parts.length,
    parts: parsed.parts,
  };
}

export function toPublicChunkedArchive(archive) {
  if (!archive) return null;
  const { parts, ...publicArchive } = archive;
  return publicArchive;
}
