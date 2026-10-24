const STATUS_LABELS = {
  IN_PROGRESS: 'قيد الرفع - لم تكتمل الأجزاء',
  COMPLETE: 'مكتمل - وصلت جميع الأجزاء وأصبح الأرشيف جاهزًا',
  CANCELLED: 'أُلغي الرفع - الأرشيف غير صالح للاستخدام',
  INCOMPLETE: 'غير مكتمل - توقف الرفع قبل وصول جميع الأجزاء',
  DELETED: 'حُذف الأرشيف - لم تعد الأجزاء متاحة',
};

export function buildUploadStatusText(session, status, note = '', now = new Date()) {
  const uploadedCount = session.uploaded.size;
  const totalParts = session.parts.length;
  const remainingParts = totalParts - uploadedCount;
  const partLines = session.parts.map((part) => {
    const marker = session.uploaded.has(part.index) ? 'وصل' : 'لم يصل';
    return `  - [${marker}] ${part.name} (${part.size} bytes)`;
  });

  return `حالة أرشيف مَخزَن\n=================\nSTATUS_CODE: ${status}\nالحالة: ${STATUS_LABELS[status] || status}\nآخر تحديث: ${now.toISOString()}\n\nبيانات الملف الأصلي\n-------------------\nاسم الملف: ${session.metadata.originalName}\nالحجم الكلي بالبايت: ${session.metadata.size}\nالحجم الكلي تقريبًا: ${(session.metadata.size / (1024 ** 3)).toFixed(2)} GiB\nمعرّف العملية: ${session.uploadId}\nطريقة التخزين: ${session.strategy === 'release' ? 'GitHub Release' : session.strategy === 'chunked' ? 'أجزاء داخل uploads/large في المستودع' : 'غير محددة'}\nمعرّف Release: ${session.releaseId || 'لا يوجد'}\nوسم الأرشيف: ${session.tag}\nمسار ملف الحالة: ${session.statusPath}\n\nالأجزاء\n-------\nالعدد الكلي: ${totalParts}\nالأجزاء التي وصلت: ${uploadedCount}\nالأجزاء المتبقية: ${remainingParts}\n${partLines.join('\n')}\n\nتنبيه\n-----\n${status === 'COMPLETE' ? 'الأرشيف مكتمل. يمكن تنزيله ودمج الأجزاء من صفحة مَخزَن.' : 'لا تعتبر هذا أرشيفًا مكتملًا ولا تخبر المستخدم أن الملف الأصلي محفوظ بالكامل. راجع علامات الأجزاء أعلاه.'}${note ? `\nملاحظة إضافية: ${note}` : ''}\n`;
}
