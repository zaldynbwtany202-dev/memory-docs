import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { once } from 'node:events';
import express from 'express';
import multer from 'multer';
import dotenv from 'dotenv';
import { GitHubStorage } from './lib/github-storage.js';
import {
  buildStoragePath,
  getArchiveExtension,
  getArchiveType,
  isValidStoragePath,
  parseStoragePath,
  sanitizeFilename,
} from './lib/file-utils.js';
import {
  createReleasePlan,
  RELEASE_PART_SIZE,
  REPOSITORY_FILE_SIZE_LIMIT,
  toPublicReleaseArchive,
} from './lib/release-archive.js';
import { buildUploadStatusText } from './lib/upload-status.js';
import {
  CHUNKED_PART_SIZE,
  createChunkedPlan,
  toChunkedArchive,
  toPublicChunkedArchive,
} from './lib/chunked-archive.js';

const rootDir = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(rootDir, '.env'), quiet: true });

const [repositoryOwner = '', repositoryName = ''] = (process.env.GITHUB_REPOSITORY || '').split('/');
const owner = (process.env.GITHUB_OWNER || repositoryOwner).trim();
const repo = (process.env.GITHUB_REPO || repositoryName).trim();
const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
const branch = (process.env.GITHUB_BRANCH || 'main').trim();
const requestedLimitGb = Number(process.env.MAX_FILE_SIZE_GB || 20);
const maxFileSizeGb = Number.isFinite(requestedLimitGb) && requestedLimitGb > 0
  ? Math.min(requestedLimitGb, 100)
  : 20;
const maxFileSize = Math.floor(maxFileSizeGb * 1024 * 1024 * 1024);
const isConfigured = Boolean(token && owner && repo && branch);
const storage = isConfigured ? new GitHubStorage({
  token,
  owner,
  repo,
  branch,
  apiUrl: process.env.GITHUB_API_URL || 'https://api.github.com',
  uploadUrl: process.env.GITHUB_UPLOAD_URL || 'https://uploads.github.com',
}) : null;
const largeUploads = new Map();

export const app = express();
app.disable('x-powered-by');

app.use((req, res, next) => {
  res.set({
    'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
    'Referrer-Policy': 'no-referrer',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
  });
  next();
});

app.use('/api', (req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});
app.use(express.json({ limit: '16kb' }));

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: REPOSITORY_FILE_SIZE_LIMIT,
    files: 1,
    fields: 0,
    parts: 2,
  },
  fileFilter: (req, file, callback) => {
    if (!getArchiveExtension(file.originalname)) {
      const error = new Error('Only ZIP and 7z files are accepted.');
      error.status = 415;
      error.publicMessage = 'صيغة الملف غير مدعومة. اختر ملفًا بامتداد ZIP أو 7Z.';
      return callback(error);
    }
    callback(null, true);
  },
});

const asyncRoute = (handler) => (req, res, next) => {
  Promise.resolve(handler(req, res, next)).catch(next);
};

function requireStorage(req, res, next) {
  if (!storage) {
    return res.status(503).json({
      error: 'لم يكتمل الاتصال بـ GitHub. أضف إعدادات المستودع ورمز الوصول في الخادم.',
      code: 'GITHUB_NOT_CONFIGURED',
    });
  }
  next();
}

const chunkedPartParser = express.raw({ type: 'application/octet-stream', limit: CHUNKED_PART_SIZE });

function parseLargePart(req, res, next) {
  if (req.largeUpload.strategy === 'chunked') return chunkedPartParser(req, res, next);
  next();
}

function requireLargeUpload(req, res, next) {
  const session = largeUploads.get(req.params.uploadId);
  if (!session) {
    return res.status(404).json({
      error: 'جلسة الرفع غير موجودة أو انتهت. ابدأ رفع الملف من جديد.',
      code: 'UPLOAD_SESSION_NOT_FOUND',
    });
  }
  req.largeUpload = session;
  next();
}

function expectedArchiveType(name) {
  return getArchiveExtension(name) === '.7z' ? '7z' : 'zip';
}

async function writeUploadStatus(session, status, note = '') {
  const text = buildUploadStatusText(session, status, note);
  await storage.upsertTextFile(
    session.statusPath,
    text,
    `chore: mark archive ${session.tag} ${status.toLowerCase()}`,
  );
}

async function tryWriteUploadStatus(session, status, note = '') {
  try {
    await writeUploadStatus(session, status, note);
  } catch (error) {
    console.warn(`Could not update status for ${session.tag}: ${error.message}`);
  }
}

app.get('/api/config', (req, res) => {
  res.json({
    configured: isConfigured,
    maxFileSize,
    maxFileSizeGb,
    repositoryFileSize: REPOSITORY_FILE_SIZE_LIMIT,
    releasePartSize: RELEASE_PART_SIZE,
    repository: owner && repo ? {
      owner,
      name: repo,
      branch,
      url: `https://github.com/${owner}/${repo}`,
    } : null,
  });
});

app.get('/api/files', requireStorage, asyncRoute(async (req, res) => {
  const [repositoryFiles, releaseArchives, chunkedArchives] = await Promise.all([
    storage.listFiles(),
    storage.listReleaseArchives(),
    storage.listChunkedArchives(),
  ]);
  const releaseFiles = releaseArchives.map(toPublicReleaseArchive);
  const chunkedFiles = chunkedArchives.map(toPublicChunkedArchive);
  const files = [...repositoryFiles, ...releaseFiles, ...chunkedFiles]
    .sort((a, b) => b.uploadedAt.localeCompare(a.uploadedAt));
  res.json({ files });
}));

// Small archives are stored directly in the repository, up to GitHub's 100 MiB limit.
app.post(
  '/api/files',
  requireStorage,
  upload.single('file'),
  asyncRoute(async (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: 'اختر ملف ZIP أو 7Z أولًا.', code: 'FILE_REQUIRED' });
    }

    const originalName = sanitizeFilename(req.file.originalname);
    const archiveType = getArchiveType(req.file.buffer);
    if (!archiveType) {
      return res.status(415).json({
        error: 'محتوى هذا الملف لا يطابق ZIP أو 7Z. اختر ملفًا مضغوطًا صالحًا.',
        code: 'INVALID_ARCHIVE',
      });
    }

    if (archiveType !== expectedArchiveType(originalName)) {
      return res.status(415).json({
        error: 'امتداد الملف لا يطابق محتواه. أعد تسميته بالامتداد الصحيح ثم حاول مجددًا.',
        code: 'ARCHIVE_TYPE_MISMATCH',
      });
    }

    const storagePath = buildStoragePath(originalName);
    const file = await storage.uploadFile(storagePath, req.file.buffer, originalName);
    res.status(201).json({ file });
  }),
);

app.get('/api/files/download', requireStorage, asyncRoute(async (req, res) => {
  const storagePath = req.query.path;
  if (!isValidStoragePath(storagePath)) {
    return res.status(400).json({ error: 'مسار الملف غير صالح.', code: 'INVALID_PATH' });
  }

  const { originalName } = parseStoragePath(storagePath);
  const contents = await storage.downloadFile(storagePath);
  res.attachment(originalName);
  res.type(expectedArchiveType(originalName) === '7z' ? 'application/x-7z-compressed' : 'application/zip');
  res.set('Content-Length', String(contents.length));
  res.send(contents);
}));

app.delete('/api/files', requireStorage, asyncRoute(async (req, res) => {
  const { path: storagePath, sha } = req.body || {};
  if (!isValidStoragePath(storagePath) || !/^[a-f0-9]{40}$/i.test(sha || '')) {
    return res.status(400).json({ error: 'بيانات الملف غير صالحة.', code: 'INVALID_FILE_DATA' });
  }

  const { originalName } = parseStoragePath(storagePath);
  await storage.deleteFile(storagePath, sha, originalName);
  res.status(204).end();
}));

// Start a chunked release upload. Only six signature bytes cross the server here;
// the large file itself remains in the browser until each Blob part is streamed.
app.post('/api/large-uploads', requireStorage, asyncRoute(async (req, res) => {
  const { name, size, signature } = req.body || {};
  if (!getArchiveExtension(name || '')) {
    return res.status(415).json({ error: 'اختر ملفًا بامتداد ZIP أو 7Z.', code: 'INVALID_FILE_TYPE' });
  }
  if (!Number.isSafeInteger(size) || size <= REPOSITORY_FILE_SIZE_LIMIT) {
    return res.status(400).json({ error: 'استخدم الرفع العادي لهذا الحجم.', code: 'SMALL_FILE_REQUIRED' });
  }
  if (size > maxFileSize) {
    return res.status(413).json({
      error: `حجم الملف أكبر من الحد المسموح (${maxFileSizeGb} ج.ب).`,
      code: 'FILE_TOO_LARGE',
    });
  }
  if (typeof signature !== 'string' || !/^[a-f0-9]{12}$/i.test(signature)) {
    return res.status(400).json({ error: 'تعذر التحقق من توقيع الملف.', code: 'INVALID_SIGNATURE' });
  }

  const originalName = sanitizeFilename(name);
  const archiveType = getArchiveType(Buffer.from(signature, 'hex'));
  if (!archiveType || archiveType !== expectedArchiveType(originalName)) {
    return res.status(415).json({
      error: 'امتداد الملف لا يطابق توقيع ZIP أو 7Z الموجود في محتواه.',
      code: 'ARCHIVE_TYPE_MISMATCH',
    });
  }

  let strategy = 'chunked';
  try {
    await storage.assertReleaseUploadsAvailable();
    strategy = 'release';
  } catch (error) {
    if (error.code !== 'RELEASE_UPLOAD_UNAVAILABLE') throw error;
  }

  let session;
  if (strategy === 'release') {
    const plan = createReleasePlan(originalName, size);
    const release = await storage.createDraftRelease(plan.metadata, plan.tag);
    const uploadUrl = typeof release.upload_url === 'string' ? release.upload_url.split('{')[0] : null;

    if (!release.id || !uploadUrl) {
      if (release.id) await storage.deleteRelease(release.id);
      const error = new Error('GitHub did not return a release upload URL.');
      error.code = 'INCOMPLETE_RELEASE';
      throw error;
    }

    session = {
      ...plan,
      strategy,
      chunkSize: RELEASE_PART_SIZE,
      releaseId: String(release.id),
      releaseUrl: release.html_url || null,
      statusPath: `uploads/status/${plan.tag}.txt`,
      uploadUrl,
      uploaded: new Map(),
      updatedAt: Date.now(),
    };
  } else {
    const plan = createChunkedPlan(originalName, size);
    session = {
      ...plan,
      strategy,
      releaseId: null,
      releaseUrl: null,
      statusPath: `uploads/status/${plan.tag}.txt`,
      uploaded: new Map(),
      updatedAt: Date.now(),
    };
  }

  try {
    await writeUploadStatus(
      session,
      'IN_PROGRESS',
      strategy === 'release' ? 'التخزين في GitHub Release.' : 'قناة Releases غير متاحة؛ ستُحفظ الأجزاء داخل المستودع.',
    );
  } catch (error) {
    if (session.strategy === 'release') {
      await storage.deleteDraftRelease(session.releaseId).catch((cleanupError) => {
        console.warn(`Could not clean draft after status failure: ${cleanupError.message}`);
      });
    }
    throw error;
  }
  largeUploads.set(session.uploadId, session);

  res.status(201).json({
    uploadId: session.uploadId,
    releaseId: session.releaseId,
    statusPath: session.statusPath,
    strategy: session.strategy,
    chunkSize: session.chunkSize,
    parts: session.parts,
  });
}));

// Stream Release parts directly to GitHub. Repository fallback parts are capped
// at 95 MiB and buffered one at a time; nothing is written to server disk.
app.post('/api/large-uploads/:uploadId/parts/:partIndex', requireStorage, requireLargeUpload, parseLargePart, asyncRoute(async (req, res) => {
  const session = req.largeUpload;
  const partIndex = Number(req.params.partIndex);
  const part = session.parts.find((item) => item.index === partIndex);
  if (!part) {
    return res.status(404).json({ error: 'رقم الجزء غير صالح.', code: 'INVALID_PART' });
  }

  const previousAsset = session.uploaded.get(partIndex);
  if (previousAsset) return res.status(200).json({ part: previousAsset });

  const contentLength = Number(req.get('content-length'));
  if (!Number.isSafeInteger(contentLength) || contentLength !== part.size) {
    return res.status(400).json({
      error: 'حجم الجزء المرسل لا يطابق خطة الرفع.',
      code: 'INVALID_PART_SIZE',
    });
  }

  req.setTimeout(0);
  res.setTimeout(0);
  session.updatedAt = Date.now();
  const asset = session.strategy === 'release'
    ? await storage.uploadReleaseAsset(session.uploadUrl, part, req)
    : await storage.uploadRepositoryPart(part.path, req.body, session.metadata.originalName);
  const uploadedPart = {
    index: partIndex,
    id: String(asset.id || asset.sha),
    name: part.name,
    path: part.path,
    size: asset.size || part.size,
  };
  session.uploaded.set(partIndex, uploadedPart);
  session.updatedAt = Date.now();
  await writeUploadStatus(session, 'IN_PROGRESS', `وصل الجزء ${partIndex + 1} من ${session.parts.length}.`);
  res.status(201).json({ part: uploadedPart });
}));

app.post('/api/large-uploads/:uploadId/complete', requireStorage, requireLargeUpload, asyncRoute(async (req, res) => {
  const session = req.largeUpload;
  if (session.uploaded.size !== session.parts.length) {
    return res.status(409).json({
      error: 'لم تكتمل جميع الأجزاء بعد.',
      code: 'PARTS_MISSING',
      uploadedParts: session.uploaded.size,
      totalParts: session.parts.length,
    });
  }

  let archive;
  if (session.strategy === 'release') {
    archive = await storage.publishRelease(session.releaseId);
  } else {
    await storage.upsertTextFile(
      session.manifestPath,
      JSON.stringify(session.metadata, null, 2),
      `chore: complete chunked archive ${session.metadata.originalName}`,
    );
    const branchPath = branch.split('/').map(encodeURIComponent).join('/');
    archive = toChunkedArchive(
      session.tag,
      session.metadata,
      `https://github.com/${owner}/${repo}/tree/${branchPath}/${session.directory}`,
    );
  }

  largeUploads.delete(session.uploadId);
  await tryWriteUploadStatus(session, 'COMPLETE', 'وصلت جميع الأجزاء وأصبح الأرشيف جاهزًا.');
  res.json({
    file: session.strategy === 'release'
      ? toPublicReleaseArchive(archive)
      : toPublicChunkedArchive(archive),
  });
}));

app.delete('/api/large-uploads/:uploadId', requireStorage, requireLargeUpload, asyncRoute(async (req, res) => {
  const session = req.largeUpload;
  let alreadyComplete = false;
  if (session.strategy === 'release') {
    const deletedDraft = await storage.deleteDraftRelease(session.releaseId);
    alreadyComplete = !deletedDraft;
  } else {
    const paths = [...session.uploaded.values()].map((part) => part.path).filter(Boolean);
    await storage.deletePaths(paths, `chore: cancel chunked archive ${session.metadata.originalName}`);
  }

  await tryWriteUploadStatus(
    session,
    alreadyComplete ? 'COMPLETE' : 'CANCELLED',
    alreadyComplete ? 'كان الإصدار منشورًا بالفعل؛ لم يُحذف.' : 'أُلغيت العملية وحُذفت الأجزاء غير المكتملة.',
  );
  largeUploads.delete(session.uploadId);
  res.status(204).end();
}));

// Join release assets in order while streaming, so the browser receives the
// original archive without the server ever holding the complete file in memory.
app.get('/api/large-files/:releaseId/download', requireStorage, asyncRoute(async (req, res) => {
  if (!/^\d+$/.test(req.params.releaseId)) {
    return res.status(400).json({ error: 'معرّف الإصدار غير صالح.', code: 'INVALID_RELEASE' });
  }

  const archive = await storage.getReleaseArchive(req.params.releaseId);
  if (!archive) {
    return res.status(404).json({ error: 'الأرشيف الكبير غير موجود أو أجزاؤه غير مكتملة.', code: 'ARCHIVE_NOT_FOUND' });
  }

  res.attachment(archive.name);
  res.type(expectedArchiveType(archive.name) === '7z' ? 'application/x-7z-compressed' : 'application/zip');
  res.set({
    'Content-Length': String(archive.size),
    'X-Accel-Buffering': 'no',
  });
  res.setTimeout(0);

  try {
    for (const asset of archive.assets) {
      if (res.destroyed) return;
      const response = await storage.downloadReleaseAsset(asset.id);
      await pipeline(Readable.fromWeb(response.body), res, { end: false });
    }
    res.end();
  } catch (error) {
    if (res.headersSent) {
      res.destroy(error);
      return;
    }
    throw error;
  }
}));

app.delete('/api/large-files/:releaseId', requireStorage, asyncRoute(async (req, res) => {
  if (!/^\d+$/.test(req.params.releaseId)) {
    return res.status(400).json({ error: 'معرّف الإصدار غير صالح.', code: 'INVALID_RELEASE' });
  }
  const deleted = await storage.deleteReleaseArchive(req.params.releaseId);
  if (!deleted) {
    return res.status(404).json({ error: 'الأرشيف المطلوب غير موجود.', code: 'ARCHIVE_NOT_FOUND' });
  }
  res.status(204).end();
}));

app.get('/api/chunked-files/:tag/download', requireStorage, asyncRoute(async (req, res) => {
  const archive = await storage.getChunkedArchive(req.params.tag);
  if (!archive) {
    return res.status(404).json({ error: 'الأرشيف المجزأ غير موجود.', code: 'ARCHIVE_NOT_FOUND' });
  }

  res.attachment(archive.name);
  res.type(expectedArchiveType(archive.name) === '7z' ? 'application/x-7z-compressed' : 'application/zip');
  res.set({ 'Content-Length': String(archive.size), 'X-Accel-Buffering': 'no' });
  res.setTimeout(0);

  try {
    for (const part of archive.parts) {
      if (res.destroyed) return;
      const contents = await storage.downloadFile(part.path);
      if (contents.length !== part.size) {
        const error = new Error(`Part size mismatch: ${part.path}`);
        error.code = 'INCOMPLETE_RELEASE';
        throw error;
      }
      if (!res.write(contents)) await once(res, 'drain');
    }
    res.end();
  } catch (error) {
    if (res.headersSent) {
      res.destroy(error);
      return;
    }
    throw error;
  }
}));

app.delete('/api/chunked-files/:tag', requireStorage, asyncRoute(async (req, res) => {
  const archive = await storage.deleteChunkedArchive(req.params.tag);
  if (!archive) {
    return res.status(404).json({ error: 'الأرشيف المجزأ غير موجود.', code: 'ARCHIVE_NOT_FOUND' });
  }

  const statusSession = {
    uploadId: `deleted-${archive.tag}`,
    strategy: 'chunked',
    releaseId: null,
    tag: archive.tag,
    statusPath: `uploads/status/${archive.tag}.txt`,
    metadata: { originalName: archive.name, size: archive.size },
    parts: archive.parts.map((part, index) => ({ ...part, index })),
    uploaded: new Map(archive.parts.map((part, index) => [index, part])),
  };
  await tryWriteUploadStatus(statusSession, 'DELETED', 'حُذفت الأجزاء والبيانات الوصفية من المستودع.');
  res.status(204).end();
}));

// Remove abandoned draft uploads after 48 hours. Each completed part extends the session.
const cleanupTimer = setInterval(async () => {
  const now = Date.now();
  for (const [uploadId, session] of largeUploads) {
    if (now - session.updatedAt < 48 * 60 * 60 * 1000) continue;
    let status = 'INCOMPLETE';
    try {
      if (session.strategy === 'release') {
        const deletedDraft = await storage?.deleteDraftRelease(session.releaseId);
        if (deletedDraft === false) status = 'COMPLETE';
      } else {
        const paths = [...session.uploaded.values()].map((part) => part.path).filter(Boolean);
        await storage?.deletePaths(paths, `chore: clean incomplete archive ${session.metadata.originalName}`);
      }
    } catch (error) {
      console.warn(`Could not clean incomplete upload ${session.uploadId}: ${error.message}`);
    }
    await tryWriteUploadStatus(session, status, 'انتهت مهلة جلسة الرفع قبل اكتمالها.');
    largeUploads.delete(uploadId);
  }
}, 6 * 60 * 60 * 1000);
cleanupTimer.unref();

app.use('/api', (req, res) => {
  res.status(404).json({ error: 'المسار المطلوب غير موجود.', code: 'NOT_FOUND' });
});

app.use(express.static(path.join(rootDir, 'public'), {
  setHeaders(res, filePath) {
    if (filePath.includes(`${path.sep}fonts${path.sep}`)) {
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    } else {
      res.setHeader('Cache-Control', 'no-cache');
    }
  },
}));

app.use((error, req, res, next) => {
  if (res.headersSent) return next(error);

  if (error.type === 'entity.too.large') {
    return res.status(413).json({ error: 'حجم الجزء أكبر من الحد المسموح.', code: 'PART_TOO_LARGE' });
  }

  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(413).json({
        error: 'الملف أكبر من 100 م.ب. استخدم النسخة الحديثة من الصفحة لرفعه مجزّأً.',
        code: 'FILE_TOO_LARGE',
      });
    }
    return res.status(400).json({ error: 'تعذر قراءة الملف المرفوع. حاول مرة أخرى.', code: error.code });
  }

  if (error.publicMessage) {
    return res.status(error.status || 400).json({ error: error.publicMessage, code: 'INVALID_FILE' });
  }

  if (error.code === 'RELEASE_UPLOAD_UNAVAILABLE') {
    return res.status(503).json({
      error: 'بيئة التشغيل لا تسمح بالوصول إلى uploads.github.com. الرفع المجزأ يحتاج خادمًا يسمح بهذا العنوان.',
      code: 'RELEASE_UPLOAD_UNAVAILABLE',
    });
  }

  if (error.code === 'INCOMPLETE_RELEASE') {
    console.error(error.message);
    return res.status(409).json({ error: 'بيانات الإصدار أو أجزاؤه غير مكتملة.', code: error.code });
  }

  if (error.message === 'fetch failed' || error.code === 'GITHUB_UNAVAILABLE') {
    console.error(error.message);
    return res.status(502).json({
      error: 'تعذر الوصول إلى GitHub. تحقق من اتصال الخادم بالشبكة ثم حاول مجددًا.',
      code: 'GITHUB_UNAVAILABLE',
    });
  }

  if (error.code === 'GITHUB_ERROR') {
    console.error(error.message);
    const messages = {
      401: 'رمز GitHub غير صالح أو منتهي. حدّث بيانات الاتصال في الخادم.',
      403: 'رفض GitHub العملية. تأكد من صلاحية contents:write ومن الحد المسموح للطلبات.',
      404: 'تعذر العثور على المستودع أو الفرع أو الملف. تحقق من الإعدادات.',
      409: 'تغيّر المستودع أثناء العملية. حدّث الصفحة وحاول مجددًا.',
      422: 'لم يقبل GitHub العملية. تحقق من الفرع وصلاحيات الرمز.',
    };
    return res.status(error.status === 404 ? 404 : 502).json({
      error: messages[error.status] || 'حدث خلل أثناء الاتصال بـ GitHub. حاول مرة أخرى.',
      code: 'GITHUB_ERROR',
    });
  }

  console.error(error);
  res.status(500).json({ error: 'حدث خطأ غير متوقع. حاول مرة أخرى.', code: 'INTERNAL_ERROR' });
});

const port = Number(process.env.PORT || 3000);
const isDirectRun = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isDirectRun) {
  const server = app.listen(port, '0.0.0.0', () => {
    console.log(`Memory Docs is ready at http://0.0.0.0:${port}`);
    console.log(isConfigured ? `GitHub archive: ${owner}/${repo} (${branch})` : 'GitHub archive: not configured');
  });

  // Each release part can be up to 1.75 GiB on a slow connection.
  server.requestTimeout = 4 * 60 * 60 * 1000;
  server.headersTimeout = 60 * 1000;
}
