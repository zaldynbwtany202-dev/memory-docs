const state = {
  config: null,
  selectedFile: null,
  files: [],
  uploading: false,
  loadingFiles: false,
  fileToDelete: null,
  toastTimer: null,
  cancelRequested: false,
  activeRequest: null,
};

const elements = {
  connectionStatus: document.querySelector('#connection-status'),
  connectionLabel: document.querySelector('#connection-label'),
  repositoryLink: document.querySelector('#repository-link'),
  repositoryName: document.querySelector('#repository-name'),
  repositoryFolderLink: document.querySelector('#repository-folder-link'),
  branchWrapper: document.querySelector('#branch-wrapper'),
  branchName: document.querySelector('#branch-name'),
  setupAlert: document.querySelector('#setup-alert'),
  uploadForm: document.querySelector('#upload-form'),
  fileInput: document.querySelector('#file-input'),
  dropZone: document.querySelector('#drop-zone'),
  selectedFile: document.querySelector('#selected-file'),
  selectedFileName: document.querySelector('#selected-file-name'),
  selectedFileMeta: document.querySelector('#selected-file-meta'),
  selectedFileType: document.querySelector('#selected-file-type'),
  removeFile: document.querySelector('#remove-file'),
  uploadButton: document.querySelector('#upload-button'),
  uploadProgress: document.querySelector('#upload-progress'),
  progressLabel: document.querySelector('#progress-label'),
  progressValue: document.querySelector('#progress-value'),
  progressTrack: document.querySelector('#progress-track'),
  cancelUpload: document.querySelector('#cancel-upload'),
  maxSizeLabel: document.querySelector('#max-size-label'),
  refreshFiles: document.querySelector('#refresh-files'),
  retryFiles: document.querySelector('#retry-files'),
  filesList: document.querySelector('#files-list'),
  filesEmpty: document.querySelector('#files-empty'),
  filesError: document.querySelector('#files-error'),
  filesErrorMessage: document.querySelector('#files-error-message'),
  filesCount: document.querySelector('#files-count'),
  deleteDialog: document.querySelector('#delete-dialog'),
  deleteFileName: document.querySelector('#delete-file-name'),
  closeDeleteDialog: document.querySelector('#close-delete-dialog'),
  cancelDelete: document.querySelector('#cancel-delete'),
  confirmDelete: document.querySelector('#confirm-delete'),
  toastContainer: document.querySelector('#toast-container'),
};

const numberFormatter = new Intl.NumberFormat('ar-DZ', { maximumFractionDigits: 1 });
const dateFormatter = new Intl.DateTimeFormat('ar-DZ', {
  day: 'numeric',
  month: 'short',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
});

function createIcon(name, extraClass = '') {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', `icon ${extraClass}`.trim());
  svg.setAttribute('aria-hidden', 'true');
  const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
  use.setAttribute('href', `#icon-${name}`);
  svg.append(use);
  return svg;
}

function formatBytes(bytes) {
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 بايت';
  const units = ['بايت', 'ك.ب', 'م.ب', 'ج.ب', 'ت.ب'];
  const unitIndex = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / (1024 ** unitIndex);
  return `${numberFormatter.format(value)} ${units[unitIndex]}`;
}

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? 'تاريخ غير متاح' : dateFormatter.format(date);
}

function getArchiveTypeLabel(name) {
  return /\.7z$/i.test(name) ? '7Z' : 'ZIP';
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (response.status === 204) return null;

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.error || 'تعذر الاتصال بالخادم. حاول مرة أخرى.');
  }
  return data;
}

function setConnection(status, label) {
  elements.connectionStatus.classList.toggle('is-loading', status === 'loading');
  elements.connectionStatus.classList.toggle('is-error', status === 'error');
  elements.connectionLabel.textContent = label;
}

function showToast(message, type = 'success') {
  window.clearTimeout(state.toastTimer);
  const toast = document.createElement('div');
  toast.className = `toast${type === 'error' ? ' is-error' : ''}`;
  toast.append(createIcon(type === 'error' ? 'alert' : 'check'));

  const text = document.createElement('span');
  text.textContent = message;
  toast.append(text);
  elements.toastContainer.replaceChildren(toast);

  state.toastTimer = window.setTimeout(() => {
    toast.classList.add('is-leaving');
    window.setTimeout(() => toast.remove(), 220);
  }, type === 'error' ? 6500 : 4500);
}

function branchUrl(repositoryUrl, branch) {
  const encodedBranch = branch.split('/').map(encodeURIComponent).join('/');
  return `${repositoryUrl}/tree/${encodedBranch}/uploads`;
}

async function loadConfig() {
  setConnection('loading', 'جارٍ الاتصال…');

  try {
    const config = await fetchJson('/api/config');
    state.config = config;
    elements.maxSizeLabel.textContent = formatBytes(config.maxFileSize);

    if (config.repository) {
      const { owner, name, branch, url } = config.repository;
      elements.repositoryName.textContent = `${owner} / ${name}`;
      elements.repositoryLink.href = url;
      elements.repositoryLink.hidden = false;
      elements.repositoryFolderLink.href = branchUrl(url, branch);
      elements.repositoryFolderLink.hidden = false;
      elements.branchName.textContent = branch;
      elements.branchWrapper.hidden = false;
    } else {
      elements.repositoryName.textContent = 'لم يتم تحديد مستودع';
    }

    elements.setupAlert.hidden = config.configured;
    if (!config.configured) {
      setConnection('error', 'GitHub غير متصل');
      showFilesError('أكمل إعدادات GitHub في الخادم لعرض الملفات المحفوظة ورفع ملفات جديدة.');
    } else {
      setConnection('connected', 'متصل بـ GitHub');
      await loadFiles();
    }
  } catch (error) {
    setConnection('error', 'تعذر الاتصال');
    elements.setupAlert.hidden = false;
    elements.repositoryName.textContent = 'الإعدادات غير متاحة';
    showFilesError(error.message);
  } finally {
    updateUploadButton();
  }
}

function updateUploadButton() {
  const isConfigured = Boolean(state.config?.configured);
  elements.uploadButton.disabled = !state.selectedFile || state.uploading || !isConfigured;
  elements.uploadButton.querySelector('span').textContent = state.uploading ? 'جارٍ الحفظ…' : 'حفظ في GitHub';
  elements.removeFile.disabled = state.uploading;
  elements.fileInput.disabled = state.uploading;
  elements.dropZone.setAttribute('aria-disabled', String(state.uploading || !isConfigured));
}

function validateFile(file) {
  if (!file) return 'لم يتم اختيار ملف.';
  if (!/\.(zip|7z)$/i.test(file.name)) return 'اختر ملفًا بامتداد ZIP أو 7Z فقط.';
  if (file.size === 0) return 'هذا الملف فارغ. اختر ملفًا مضغوطًا صالحًا.';

  const maxFileSize = state.config?.maxFileSize || (20 * 1024 * 1024 * 1024);
  if (file.size > maxFileSize) {
    return `حجم الملف ${formatBytes(file.size)}، بينما الحد المسموح ${formatBytes(maxFileSize)}.`;
  }
  return null;
}

function selectFile(file) {
  const validationError = validateFile(file);
  if (validationError) {
    showToast(validationError, 'error');
    elements.fileInput.value = '';
    return;
  }

  state.selectedFile = file;
  elements.selectedFileName.textContent = file.name;
  elements.selectedFileName.title = file.name;
  const isLarge = state.config && file.size > state.config.repositoryFileSize;
  const planLabel = isLarge ? 'سيُقسّم تلقائيًا أثناء الرفع' : 'جاهز للرفع';
  elements.selectedFileMeta.textContent = `${formatBytes(file.size)} · ${planLabel}`;
  elements.selectedFileType.textContent = getArchiveTypeLabel(file.name);
  elements.dropZone.hidden = true;
  elements.selectedFile.hidden = false;
  resetProgress();
  updateUploadButton();
}

function clearSelection() {
  if (state.uploading) return;
  state.selectedFile = null;
  elements.fileInput.value = '';
  elements.selectedFile.hidden = true;
  elements.dropZone.hidden = false;
  resetProgress();
  updateUploadButton();
}

function resetProgress() {
  elements.uploadProgress.hidden = true;
  elements.uploadProgress.classList.remove('is-saving');
  elements.progressTrack.value = 0;
  elements.progressTrack.textContent = '0%';
  elements.progressValue.textContent = '0%';
  elements.progressLabel.textContent = 'جارٍ رفع الملف…';
  elements.progressTrack.setAttribute('aria-valuenow', '0');
  elements.cancelUpload.hidden = true;
  elements.cancelUpload.disabled = false;
}

function setProgress(percent) {
  const safePercent = Math.max(0, Math.min(100, Math.round(percent)));
  elements.uploadProgress.hidden = false;
  elements.uploadProgress.classList.remove('is-saving');
  elements.progressTrack.value = safePercent;
  elements.progressTrack.textContent = `${safePercent}%`;
  elements.progressValue.textContent = `${numberFormatter.format(safePercent)}%`;
  elements.progressTrack.setAttribute('aria-valuenow', String(safePercent));
}

function setSavingProgress(label = 'اكتمل الرفع، جارٍ الحفظ في GitHub…') {
  elements.uploadProgress.hidden = false;
  elements.uploadProgress.classList.add('is-saving');
  elements.progressLabel.textContent = label;
  elements.progressValue.textContent = '100%';
  elements.progressTrack.removeAttribute('value');
  elements.progressTrack.removeAttribute('aria-valuenow');
}

function sendFile(file) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    const data = new FormData();
    data.append('file', file, file.name);

    request.open('POST', '/api/files');
    request.timeout = 15 * 60 * 1000;

    request.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        setProgress((event.loaded / event.total) * 100);
        if (event.loaded === event.total) setSavingProgress();
      }
    });
    request.upload.addEventListener('load', () => setSavingProgress());

    request.addEventListener('load', () => {
      let response = null;
      try {
        response = JSON.parse(request.responseText);
      } catch {
        response = null;
      }

      if (request.status >= 200 && request.status < 300 && response?.file) {
        resolve(response.file);
      } else {
        reject(new Error(response?.error || 'تعذر حفظ الملف. حاول مرة أخرى.'));
      }
    });
    request.addEventListener('error', () => reject(new Error('انقطع الاتصال أثناء الرفع. تحقق من الشبكة وحاول مجددًا.')));
    request.addEventListener('timeout', () => reject(new Error('استغرق الرفع وقتًا طويلًا. تحقق من الشبكة وحاول مجددًا.')));
    request.send(data);
  });
}

async function readArchiveSignature(file) {
  const bytes = new Uint8Array(await file.slice(0, 6).arrayBuffer());
  return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
}

function sendLargePart(session, part, file, completedBytes) {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    const start = part.index * session.chunkSize;
    const blob = file.slice(start, start + part.size);

    request.open('POST', `/api/large-uploads/${session.uploadId}/parts/${part.index}`);
    request.setRequestHeader('Content-Type', 'application/octet-stream');
    request.timeout = 4 * 60 * 60 * 1000;
    state.activeRequest = request;

    request.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        setProgress(((completedBytes + event.loaded) / file.size) * 100);
      }
    });
    request.addEventListener('load', () => {
      let response = null;
      try {
        response = JSON.parse(request.responseText);
      } catch {
        response = null;
      }
      if (request.status >= 200 && request.status < 300) {
        resolve(response?.part);
      } else {
        reject(new Error(response?.error || `تعذر رفع الجزء ${part.index + 1}.`));
      }
    });
    request.addEventListener('error', () => reject(new Error('انقطع الاتصال أثناء رفع أحد الأجزاء.')));
    request.addEventListener('timeout', () => reject(new Error('استغرق رفع الجزء وقتًا طويلًا. حاول مجددًا.')));
    request.addEventListener('abort', () => reject(new Error('تم إلغاء الرفع.')));
    request.addEventListener('loadend', () => {
      if (state.activeRequest === request) state.activeRequest = null;
    });
    request.send(blob);
  });
}

async function sendLargeFile(file) {
  let uploadId = null;

  try {
    const signature = await readArchiveSignature(file);
    const session = await fetchJson('/api/large-uploads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: file.name, size: file.size, signature }),
    });
    uploadId = session.uploadId;
    let completedBytes = 0;

    for (const part of session.parts) {
      if (state.cancelRequested) throw new Error('تم إلغاء الرفع.');
      elements.progressLabel.textContent = `جارٍ رفع الجزء ${numberFormatter.format(part.index + 1)} من ${numberFormatter.format(session.parts.length)}…`;
      await sendLargePart(session, part, file, completedBytes);
      completedBytes += part.size;
      setProgress((completedBytes / file.size) * 100);
    }

    elements.cancelUpload.disabled = true;
    setSavingProgress('اكتمل رفع الأجزاء، جارٍ نشر الأرشيف في GitHub…');
    const result = await fetchJson(`/api/large-uploads/${uploadId}/complete`, { method: 'POST' });
    return result.file;
  } catch (error) {
    if (uploadId) {
      try {
        const outcome = state.cancelRequested ? 'cancelled' : 'incomplete';
        await fetchJson(`/api/large-uploads/${uploadId}?outcome=${outcome}`, { method: 'DELETE' });
      } catch (cleanupError) {
        console.warn('Could not clean the incomplete upload:', cleanupError);
      }
    }
    throw error;
  } finally {
    state.activeRequest = null;
    elements.cancelUpload.disabled = false;
  }
}

function cancelLargeUpload() {
  if (!state.uploading) return;
  state.cancelRequested = true;
  elements.cancelUpload.disabled = true;
  state.activeRequest?.abort();
}

async function handleUpload(event) {
  event.preventDefault();
  if (state.uploading) return;

  if (!state.config?.configured) {
    showToast('أكمل إعدادات GitHub أولًا.', 'error');
    return;
  }

  const validationError = validateFile(state.selectedFile);
  if (validationError) {
    showToast(validationError, 'error');
    return;
  }

  const file = state.selectedFile;
  const isLarge = file.size > state.config.repositoryFileSize;
  state.uploading = true;
  state.cancelRequested = false;
  elements.cancelUpload.hidden = !isLarge;
  setProgress(0);
  updateUploadButton();

  try {
    if (isLarge) {
      await sendLargeFile(file);
    } else {
      await sendFile(file);
    }
    showToast(`تم حفظ «${file.name}» في GitHub بنجاح.`);
    state.uploading = false;
    clearSelection();
    await loadFiles({ silent: true });
  } catch (error) {
    state.uploading = false;
    elements.uploadProgress.hidden = true;
    updateUploadButton();
    showToast(
      state.cancelRequested ? 'تم إلغاء الرفع.' : error.message,
      state.cancelRequested ? 'success' : 'error',
    );
  }
}

function showSkeletons() {
  elements.filesList.hidden = false;
  elements.filesEmpty.hidden = true;
  elements.filesError.hidden = true;
  elements.filesList.setAttribute('aria-busy', 'true');
  elements.filesList.replaceChildren();

  for (let index = 0; index < 3; index += 1) {
    const row = document.createElement('div');
    row.className = 'skeleton-row';
    row.append(document.createElement('span'), document.createElement('span'), document.createElement('span'));
    elements.filesList.append(row);
  }
}

function showFilesError(message) {
  elements.filesList.hidden = true;
  elements.filesEmpty.hidden = true;
  elements.filesError.hidden = false;
  elements.filesErrorMessage.textContent = message;
  elements.filesList.setAttribute('aria-busy', 'false');
  elements.filesCount.hidden = true;
}

function buildFileRow(file) {
  const row = document.createElement('article');
  row.className = 'file-row';
  row.dataset.path = file.path;

  const main = document.createElement('div');
  main.className = 'file-main';
  const typeIcon = document.createElement('div');
  typeIcon.className = 'file-type-icon';
  typeIcon.append(createIcon('file'));
  const archiveLabel = document.createElement('small');
  archiveLabel.textContent = getArchiveTypeLabel(file.name);
  typeIcon.append(archiveLabel);

  const copy = document.createElement('div');
  copy.className = 'file-copy';
  const name = document.createElement('strong');
  name.className = 'file-name';
  name.textContent = file.name;
  name.title = file.name;
  name.dir = 'auto';
  const type = document.createElement('span');
  type.textContent = file.kind === 'release'
    ? `${numberFormatter.format(file.partCount)} أجزاء · GitHub Release`
    : file.kind === 'chunked'
      ? `${numberFormatter.format(file.partCount)} أجزاء · داخل المستودع`
      : 'ملف مضغوط · محفوظ في GitHub';
  copy.append(name, type);
  main.append(typeIcon, copy);

  const size = document.createElement('span');
  size.className = 'file-size';
  size.dataset.label = 'الحجم:';
  size.textContent = formatBytes(file.size);

  const date = document.createElement('time');
  date.className = 'file-date';
  date.dataset.label = 'التاريخ:';
  date.dateTime = file.uploadedAt;
  date.textContent = formatDate(file.uploadedAt);

  const actions = document.createElement('div');
  actions.className = 'file-actions';

  const download = document.createElement('a');
  download.className = 'icon-button download-action';
  download.href = file.downloadUrl;
  download.download = file.name;
  download.title = file.kind === 'release' || file.kind === 'chunked' ? 'تنزيل ودمج الأجزاء' : 'تنزيل الملف';
  download.setAttribute('aria-label', `${download.title} ${file.name}`);
  download.append(createIcon('download'));

  const github = document.createElement('a');
  github.className = 'icon-button';
  github.href = file.htmlUrl || '#';
  github.target = '_blank';
  github.rel = 'noopener noreferrer';
  github.title = 'عرض في GitHub';
  github.setAttribute('aria-label', `عرض ${file.name} في GitHub`);
  github.hidden = !file.htmlUrl;
  github.append(createIcon('external'));

  const remove = document.createElement('button');
  remove.className = 'icon-button delete-action';
  remove.type = 'button';
  remove.title = 'حذف الملف';
  remove.setAttribute('aria-label', `حذف ${file.name}`);
  remove.append(createIcon('trash'));
  remove.addEventListener('click', () => openDeleteDialog(file));

  actions.append(download, github, remove);
  row.append(main, size, date, actions);
  return row;
}

function renderFiles() {
  elements.filesList.replaceChildren();
  elements.filesList.setAttribute('aria-busy', 'false');
  elements.filesError.hidden = true;
  elements.filesCount.textContent = numberFormatter.format(state.files.length);
  elements.filesCount.hidden = state.files.length === 0;

  if (state.files.length === 0) {
    elements.filesList.hidden = true;
    elements.filesEmpty.hidden = false;
    return;
  }

  elements.filesEmpty.hidden = true;
  elements.filesList.hidden = false;
  const fragment = document.createDocumentFragment();
  state.files.forEach((file) => fragment.append(buildFileRow(file)));
  elements.filesList.append(fragment);
}

async function loadFiles({ silent = false } = {}) {
  if (state.loadingFiles || !state.config?.configured) return;
  state.loadingFiles = true;
  elements.refreshFiles.classList.add('is-loading');
  elements.refreshFiles.disabled = true;

  if (!silent || state.files.length === 0) showSkeletons();

  try {
    const data = await fetchJson('/api/files');
    state.files = data.files || [];
    renderFiles();
    setConnection('connected', 'متصل بـ GitHub');
  } catch (error) {
    if (!silent || state.files.length === 0) showFilesError(error.message);
    setConnection('error', 'مشكلة في الاتصال');
    if (silent) showToast(error.message, 'error');
  } finally {
    state.loadingFiles = false;
    elements.refreshFiles.classList.remove('is-loading');
    elements.refreshFiles.disabled = false;
  }
}

function openDeleteDialog(file) {
  state.fileToDelete = file;
  elements.deleteFileName.textContent = `«${file.name}»`;
  elements.confirmDelete.disabled = false;
  elements.cancelDelete.disabled = false;
  elements.confirmDelete.textContent = 'نعم، احذف الملف';
  elements.deleteDialog.showModal();
  document.body.classList.add('modal-open');
}

function closeDeleteDialog() {
  if (elements.confirmDelete.disabled) return;
  elements.deleteDialog.close();
}

async function deleteSelectedFile() {
  const file = state.fileToDelete;
  if (!file) return;

  elements.confirmDelete.disabled = true;
  elements.cancelDelete.disabled = true;
  elements.closeDeleteDialog.disabled = true;
  elements.confirmDelete.textContent = 'جارٍ الحذف…';

  try {
    if (file.kind === 'release') {
      await fetchJson(`/api/large-files/${file.releaseId}`, { method: 'DELETE' });
    } else if (file.kind === 'chunked') {
      await fetchJson(`/api/chunked-files/${encodeURIComponent(file.tag)}`, { method: 'DELETE' });
    } else {
      await fetchJson('/api/files', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: file.path, sha: file.sha }),
      });
    }

    state.files = state.files.filter((item) => item.path !== file.path);
    elements.deleteDialog.close();
    renderFiles();
    showToast(`تم حذف «${file.name}» من الأرشيف.`);
  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    elements.confirmDelete.disabled = false;
    elements.cancelDelete.disabled = false;
    elements.closeDeleteDialog.disabled = false;
    elements.confirmDelete.textContent = 'نعم، احذف الملف';
  }
}

let dragDepth = 0;

elements.dropZone.addEventListener('click', () => {
  if (state.uploading) return;
  if (!state.config?.configured) {
    showToast('أكمل إعدادات GitHub في الخادم أولًا.', 'error');
    return;
  }
  elements.fileInput.click();
});

elements.fileInput.addEventListener('change', () => selectFile(elements.fileInput.files[0]));
elements.removeFile.addEventListener('click', clearSelection);
elements.uploadForm.addEventListener('submit', handleUpload);
elements.cancelUpload.addEventListener('click', cancelLargeUpload);
elements.refreshFiles.addEventListener('click', () => loadFiles());
elements.retryFiles.addEventListener('click', () => loadFiles());

elements.dropZone.addEventListener('dragenter', (event) => {
  event.preventDefault();
  if (state.uploading) return;
  dragDepth += 1;
  elements.dropZone.classList.add('is-dragging');
});

elements.dropZone.addEventListener('dragover', (event) => {
  event.preventDefault();
  if (event.dataTransfer) event.dataTransfer.dropEffect = 'copy';
});

elements.dropZone.addEventListener('dragleave', (event) => {
  event.preventDefault();
  dragDepth = Math.max(0, dragDepth - 1);
  if (dragDepth === 0) elements.dropZone.classList.remove('is-dragging');
});

elements.dropZone.addEventListener('drop', (event) => {
  event.preventDefault();
  dragDepth = 0;
  elements.dropZone.classList.remove('is-dragging');
  if (state.uploading) return;
  if (!state.config?.configured) {
    showToast('أكمل إعدادات GitHub في الخادم أولًا.', 'error');
    return;
  }
  selectFile(event.dataTransfer?.files[0]);
});

elements.closeDeleteDialog.addEventListener('click', closeDeleteDialog);
elements.cancelDelete.addEventListener('click', closeDeleteDialog);
elements.confirmDelete.addEventListener('click', deleteSelectedFile);
elements.deleteDialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  state.fileToDelete = null;
  elements.closeDeleteDialog.disabled = false;
});
elements.deleteDialog.addEventListener('cancel', (event) => {
  if (elements.confirmDelete.disabled) event.preventDefault();
});

loadConfig();
