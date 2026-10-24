import { randomBytes } from 'node:crypto';

const STORAGE_PREFIX = 'uploads';
const STORED_FILE_PATTERN = /^uploads\/(\d{13})-([a-f0-9]{8})-(.+\.(?:zip|7z))$/i;
const ARCHIVE_EXTENSION_PATTERN = /\.(zip|7z)$/i;

/** Busboy can expose UTF-8 filenames as latin1. Repair them when possible. */
export function decodeUploadName(name) {
  if (typeof name !== 'string' || !/[À-ÿ]/.test(name)) return name;

  const decoded = Buffer.from(name, 'latin1').toString('utf8');
  return decoded.includes('\uFFFD') ? name : decoded;
}

export function getArchiveExtension(name) {
  const match = typeof name === 'string' ? name.match(ARCHIVE_EXTENSION_PATTERN) : null;
  return match ? `.${match[1].toLowerCase()}` : null;
}

/** Return a short, cross-platform filename without allowing path traversal. */
export function sanitizeFilename(input) {
  const decoded = decodeUploadName(String(input || 'archive.zip'));
  const basename = decoded.split(/[\\/]/).pop() || 'archive.zip';
  const cleaned = basename
    .normalize('NFC')
    .replace(/[<>:"/\\|?*\u0000-\u001F\u007F]/g, '-')
    .replace(/\s+/g, ' ')
    .replace(/^[.\s]+|[.\s]+$/g, '');

  const supportedExtension = getArchiveExtension(cleaned);
  const extension = supportedExtension || '.zip';
  const withoutExtension = supportedExtension ? cleaned.slice(0, -supportedExtension.length) : cleaned;
  const base = Array.from(withoutExtension || 'archive').slice(0, 140).join('');
  return `${base}${extension}`;
}

export function buildStoragePath(originalName, options = {}) {
  const timestamp = options.timestamp ?? Date.now();
  const suffix = options.suffix ?? randomBytes(4).toString('hex');
  return `${STORAGE_PREFIX}/${timestamp}-${suffix}-${sanitizeFilename(originalName)}`;
}

export function parseStoragePath(path) {
  const match = typeof path === 'string' ? path.match(STORED_FILE_PATTERN) : null;
  if (!match) return null;

  const timestamp = Number(match[1]);
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return null;

  return {
    uploadedAt: date.toISOString(),
    originalName: match[3],
  };
}

export function isValidStoragePath(path) {
  return Boolean(
    parseStoragePath(path)
    && path.length <= 320
    && !/[\u0000-\u001F\u007F]/.test(path),
  );
}

/** Identify supported archives by signature rather than trusting their extension. */
export function getArchiveType(buffer) {
  if (!Buffer.isBuffer(buffer) || buffer.length < 4) return null;

  // 7z files always begin with this six-byte signature.
  const sevenZipSignature = [0x37, 0x7a, 0xbc, 0xaf, 0x27, 0x1c];
  if (buffer.length >= 6 && sevenZipSignature.every((byte, index) => buffer[index] === byte)) {
    return '7z';
  }

  // ZIP local-file, empty-archive, and spanned-archive signatures.
  const zipSignatures = [0x04034b50, 0x06054b50, 0x08074b50];
  return zipSignatures.includes(buffer.readUInt32LE(0)) ? 'zip' : null;
}

export function toPublicFile(item) {
  if (!item || item.type !== 'file' || !parseStoragePath(item.path)) return null;

  const metadata = parseStoragePath(item.path);
  return {
    kind: 'repository',
    name: metadata.originalName,
    path: item.path,
    size: item.size || 0,
    sha: item.sha,
    uploadedAt: metadata.uploadedAt,
    htmlUrl: item.html_url || null,
    downloadUrl: `/api/files/download?path=${encodeURIComponent(item.path)}`,
  };
}
