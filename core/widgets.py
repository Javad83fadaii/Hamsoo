"""ویجت‌های اختصاصی فرم‌ها."""

import datetime

import jdatetime
from django import forms

PERSIAN_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')


class JalaliDateInput(forms.DateInput):
    """ورودی تاریخ شمسی برای پنل مدیریت.

    تاریخ را به شکل «۱۴۰۵/۰۸/۱۳» نمایش می‌دهد و همان قالب (با ارقام
    فارسی یا لاتین) را می‌پذیرد؛ ذخیره در دیتابیس مثل قبل میلادی است.
    """

    input_type = 'text'

    def format_value(self, value):
        """ارزش میلادی را برای نمایش به شمسی تبدیل می‌کند."""
        value = super().format_value(value)
        if not value:
            return ''
        try:
            gregorian = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return value
        jalali = jdatetime.date.fromgregorian(date=gregorian)
        return jalali.strftime('%Y/%m/%d').translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))

    def value_from_datadict(self, data, files, name):
        """ورودی شمسی کاربر را به رشته‌ی میلادی برای اعتبارسنجی تبدیل می‌کند."""
        raw = data.get(name)
        if not raw:
            return raw
        raw = str(raw).strip().translate(PERSIAN_DIGITS).replace('/', '-')
        parts = raw.split('-')
        if len(parts) == 3:
            try:
                year, month, day = (int(part) for part in parts)
                return jdatetime.date(year, month, day).togregorian().strftime('%Y-%m-%d')
            except ValueError:
                return raw  # بگذارید اعتبارسنجی فیلد پیام خطا بدهد
        return raw
