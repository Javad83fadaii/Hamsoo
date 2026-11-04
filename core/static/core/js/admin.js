/* ==========================================================================
   اسکریپت پنل مدیریت رسانه همسو
   - کلیک روی سطرهای جدول نتایج برای ورود سریع به صفحه ویرایش
   (بدون تغییر در رفتار چک‌باکس‌ها، لینک‌ها و دکمه‌های موجود)
   ========================================================================== */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var table = document.getElementById('result_list');
    if (!table) {
      return;
    }

    table.querySelectorAll('tbody tr').forEach(function (row) {
      // لینک اصلی سطر: معمولاً ستون اول به صفحه تغییر متصل است
      var link = row.querySelector('th a, td a');
      if (!link) {
        return;
      }

      row.classList.add('hamsoo-row-link');
      row.addEventListener('click', function (event) {
        var target = event.target;
        if (
          target.closest(
            'a, button, input, select, label, textarea, .deletelink, form'
          )
        ) {
          return; // تعامل‌های عادی دست‌نخورده می‌مانند
        }
        window.location.assign(link.href);
      });
    });
  });
})();
