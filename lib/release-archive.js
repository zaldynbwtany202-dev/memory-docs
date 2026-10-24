import { randomUUID } from 'node:crypto';

export const REPOSITORY_FILE_SIZE_LIMIT = 100 * 1024 * 1024;
export const RELEASE_PART_SIZE = Math.floor(1.75 * 1024 * 1024 * 1024);
export const MAX_RELEASE_ASSETS = 1000;
export const RELEASE_TAG_PREFIX = 'memory-docs-';

const METADATA_MARKER = 'memory-docs-archive';
const METADATA_PATTERN = /<!-- memory-docs-archive\s*\n([\s\S]*?)\n-->/;

export function createReleasePlan(originalName, size, options = {}) {
  if (!Number.isSafeInteger(size) || size <= 0) {
    throw new TypeError('Archive size must be a positive safe integer.');
  }

  const partCount = Math.ceil(size / RELEASE_PART_SIZE);
  if (partCount > MAX_RELEASE_ASSETS) {
    throw new RangeError('Archive needs more than 1,000 release assets.');
  }

  const uploadId = options.uploadId || randomUUID();
  const timestamp = options.timestamp || Date.now();
  const tag = `${RELEASE_TAG_PREFIX}${timestamp}-${uploadId.slice(0, 8)}`;
  const parts = Array.from({ length: partCount }, (_, index) => ({
    index,
    name: `${tag}.part${String(index + 1).padStart(3, '0')}`,
    size: Math.min(RELEASE_PART_SIZE, size - (index * RELEASE_PART_SIZE)),
  }));
  const metadata = {
    version: 1,
    originalName,
    size,
    uploadedAt: new Date(timestamp).toISOString(),
    partSize: RELEASE_PART_SIZE,
    parts: parts.map((part) => part.name),
  };

  return { uploadId, tag, parts, metadata };
}

export function serializeReleaseMetadata(metadata) {
  return `<!-- ${METADATA_MARKER}\n${JSON.stringify(metadata)}\n-->`;
}

export function parseReleaseMetadata(body) {
  const match = typeof body === 'string' ? body.match(METADATA_PATTERN) : null;
  if (!match) return null;

  try {
    const metadata = JSON.parse(match[1]);
    const valid = metadata.version === 1
      && typeof metadata.originalName === 'string'
      && Number.isSafeInteger(metadata.size)
      && metadata.size > 0
      && Array.isArray(metadata.parts)
      && metadata.parts.length > 0
      && metadata.parts.length <= MAX_RELEASE_ASSETS
      && metadata.parts.every((name) => typeof name === 'string' && name.length > 0);
    return valid ? metadata : null;
  } catch {
    return null;
  }
}

/** Convert a GitHub release into an archive, retaining assets for server-side merging. */
export function toReleaseArchive(release) {
  if (!release || release.draft) return null;
  const metadata = parseReleaseMetadata(release.body);
  if (!metadata || !release.tag_name?.startsWith(RELEASE_TAG_PREFIX)) return null;

  const assetsByName = new Map((release.assets || []).map((asset) => [asset.name, asset]));
  const assets = metadata.parts.map((name) => assetsByName.get(name));
  if (assets.some((asset) => !asset || asset.state && asset.state !== 'uploaded')) return null;

  const totalAssetSize = assets.reduce((total, asset) => total + asset.size, 0);
  if (totalAssetSize !== metadata.size) return null;

  return {
    kind: 'release',
    releaseId: String(release.id),
    tag: release.tag_name,
    name: metadata.originalName,
    path: `releases/${release.id}`,
    size: metadata.size,
    uploadedAt: metadata.uploadedAt || release.created_at,
    htmlUrl: release.html_url || null,
    downloadUrl: `/api/large-files/${release.id}/download`,
    partCount: assets.length,
    assets: assets.map((asset, index) => ({
      id: String(asset.id),
      name: asset.name,
      index,
      size: asset.size,
    })),
  };
}

export function toPublicReleaseArchive(archive) {
  if (!archive) return null;
  const { assets, tag, ...publicArchive } = archive;
  return publicArchive;
}
