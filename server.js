import path from 'node:path';
import { fileURLToPath } from 'node:url';
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

const rootDir = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.join(rootDir, '.env'), quiet: true });

const [repositoryOwner = '', repositoryName = ''] = (process.env.GITHUB_REPOSITORY || '').split('/');
const owner = (process.env.GITHUB_OWNER || repositoryOwner).trim();
const repo = (process.env.GITHUB_REPO || repositoryName).trim();
const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || '';
const branch = (process.env.GITHUB_BRANCH || 'main').trim();
const requestedLimit = Number(process.env.MAX_FILE_SIZE_MB || 100);
const maxFileSizeMb = Number.isFinite(requestedLimit) && requestedLimit > 0
  ? Math.min(requestedLimit, 100)
  : 100;
const maxFileSize = Math.floor(maxFileSizeMb * 1024 * 1024);
const isConfigured = Boolean(token && owner && repo && branch);
const storage = isConfigured ? new GitHubStorage({ token, owner, repo, branch }) : null;

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
app.use(express.json({ limit: '12kb' }));

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: maxFileSize,
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

app.get('/api/config', (req, res) => {
  res.json({
    configured: isConfigured,
    maxFileSize,
    maxFileSizeMb,
    repository: owner && repo ? {
      owner,
      name: repo,
      branch,
      url: `https://github.com/${owner}/${repo}`,
    } : null,
  });
});

app.get('/api/files', requireStorage, asyncRoute(async (req, res) => {
  const files = await storage.listFiles();
  res.json({ files });
}));

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

    const expectedType = getArchiveExtension(originalName) === '.7z' ? '7z' : 'zip';
    if (archiveType !== expectedType) {
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
  res.type(getArchiveExtension(originalName) === '.7z' ? 'application/x-7z-compressed' : 'application/zip');
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

app.use('/api', (req, res) => {
  res.status(404).json({ error: 'المسار المطلوب غير موجود.', code: 'NOT_FOUND' });
});

app.use(express.static(path.join(rootDir, 'public'), {
  setHeaders(res, filePath) {
    if (filePath.includes(`${path.sep}fonts${path.sep}`)) {
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    } else {
      // Revalidate HTML, CSS, and JS so newly supported formats appear immediately.
      res.setHeader('Cache-Control', 'no-cache');
    }
  },
}));

app.use((error, req, res, next) => {
  if (res.headersSent) return next(error);

  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(413).json({
        error: `حجم الملف أكبر من الحد المسموح (${maxFileSizeMb} م.ب).`,
        code: 'FILE_TOO_LARGE',
      });
    }
    return res.status(400).json({ error: 'تعذر قراءة الملف المرفوع. حاول مرة أخرى.', code: error.code });
  }

  if (error.publicMessage) {
    return res.status(error.status || 400).json({ error: error.publicMessage, code: 'INVALID_FILE' });
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

  // Allow enough time for a 100 MiB archive on slower connections.
  server.requestTimeout = 15 * 60 * 1000;
  server.headersTimeout = 60 * 1000;
}
