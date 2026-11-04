"""فیلترهای قالب برای تبدیل تاریخ میلادی به شمسی.

نمونه استفاده:
    {% load jalali %}
    {{ obj.published_at|shamsi }}          → ۱۳ آبان ۱۴۰۵
    {{ obj.created_at|shamsi }}            → ۱۳ آبان ۱۴۰۵، ساعت ۰۹:۳۰
    {% jalali_now as today %}              → تاریخ امروز به شمسی
"""

import datetime

import jdatetime
from django import template
from django.utils import timezone

register = template.Library()

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

DATE_FMT = '%d %B %Y'
DATETIME_FMT = '%d %B %Y، ساعت %H:%M'


@register.filter(name='shamsi')
def shamsi(value, arg=''):
    """تاریخ یا تاریخ‌وزمان میلادی را به قالب شمسی (با ارقام فارسی) نمایش می‌دهد."""
    if value is None or value == '':
        return ''

    if isinstance(value, datetime.datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        jalali = jdatetime.datetime.fromgregorian(datetime=value)
        default_fmt = DATETIME_FMT
    elif isinstance(value, datetime.date):
        jalali = jdatetime.date.fromgregorian(date=value)
        default_fmt = DATE_FMT
    else:
        return value

    return str(jalali.strftime(arg or default_fmt)).translate(PERSIAN_DIGITS)


@register.simple_tag
def jalali_now(fmt=''):
    """تاریخ لحظه‌ی جاری به شمسی."""
    return shamsi(timezone.localtime(timezone.now()), fmt)
