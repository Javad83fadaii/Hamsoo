"""مدل‌های محتوایی رسانه همسو.

همه‌ی متن‌ها، پادکست‌ها، ویدئوها، نشریات، اخبار، پرونده‌های مطالبه‌گری،
اعضای تیم و تنظیمات کلی سایت از این‌جا مدیریت می‌شوند و از طریق
پنل مدیریت (فقط کاربر سوپر یوزر) قابل ویرایش هستند.
"""

import jdatetime
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def to_persian_digits(value):
    """ارقام لاتین را به ارقام فارسی تبدیل می‌کند."""
    if value is None or value == '':
        return ''
    return str(value).translate(PERSIAN_DIGITS)


def gregorian_to_jalali_label(value):
    """تاریخ میلادی را به شکل «۲۵ مهر ۱۴۰۳» برمی‌گرداند."""
    if not value:
        return ''
    jalali = jdatetime.date.fromgregorian(date=value)
    return to_persian_digits(jalali.strftime('%d %B %Y'))


class TimeStampedModel(models.Model):
    """پایه‌ی مشترک برای نگه‌داشتن تاریخ ثبت و آخرین ویرایش."""

    created_at = models.DateTimeField('تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField('آخرین ویرایش', auto_now=True)

    class Meta:
        abstract = True


class PublishableQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(TimeStampedModel):
    """پایه‌ی مشترک محتوای قابل انتشار در سایت."""

    is_published = models.BooleanField(
        'نمایش در سایت',
        default=True,
        help_text='در صورت غیرفعال بودن، این مورد در سایت نمایش داده نمی‌شود.',
    )
    order = models.PositiveIntegerField(
        'ترتیب نمایش',
        default=0,
        help_text='عدد کوچک‌تر بالاتر نمایش داده می‌شود.',
    )
    published_at = models.DateField('تاریخ انتشار', default=timezone.localdate)
    date_label = models.CharField(
        'برچسب تاریخ (اختیاری)',
        max_length=40,
        blank=True,
        help_text='مثال: پاییز ۱۴۰۳. اگر خالی بماند، تاریخ شمسی خودکار ساخته می‌شود.',
    )

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def display_date(self):
        return self.date_label or gregorian_to_jalali_label(self.published_at)


class Podcast(PublishableModel):
    """قسمت‌های پادکست صوتی."""

    kind = 'podcast'

    title = models.CharField('عنوان قسمت', max_length=200)
    episode_number = models.PositiveIntegerField('شماره قسمت', null=True, blank=True)
    kind_label = models.CharField(
        'برچسب نوع',
        max_length=80,
        default='پادکست صوتی',
        help_text='متن کوچک بالای عنوان، مثال: پادکست گفتگومحور',
    )
    summary = models.TextField('توضیح کوتاه')
    audio_file = models.FileField(
        'فایل صوتی (آپلود)',
        upload_to='podcasts/',
        blank=True,
        null=True,
        help_text='فایل mp3 یا m4a را این‌جا بارگذاری کنید.',
    )
    audio_url = models.URLField(
        'یا لینک فایل صوتی',
        blank=True,
        help_text='اگر فایل را جای دیگری میزبانی می‌کنید، لینک مستقیم آن را وارد کنید.',
    )
    duration = models.CharField(
        'مدت زمان',
        max_length=12,
        blank=True,
        help_text='مثال: ۲۱:۴۰',
    )

    class Meta:
        verbose_name = 'پادکست'
        verbose_name_plural = 'پادکست‌ها'
        ordering = ('order', '-published_at', '-id')

    def __str__(self):
        return self.title

    @property
    def audio_source(self):
        """آدرس نهایی فایل صوتی (آپلود داخلی در اولویت است)."""
        if self.audio_file:
            return self.audio_file.url
        return self.audio_url

    @property
    def episode_label(self):
        if self.episode_number is None:
            return ''
        return f'قسمت {to_persian_digits(self.episode_number)}'


class Video(PublishableModel):
    """ویدئوها و مستندهای تصویری."""

    kind = 'video'

    title = models.CharField('عنوان ویدئو', max_length=200)
    category_label = models.CharField(
        'برچسب بالای عنوان',
        max_length=80,
        default='مستند گزارش میدانی',
    )
    summary = models.TextField('توضیح کوتاه')
    thumbnail = models.ImageField(
        'تصویر شاخص',
        upload_to='videos/',
        blank=True,
        null=True,
        help_text='تصویر پیش‌نمایش کارت ویدئو (اختیاری).',
    )
    video_url = models.URLField(
        'لینک ویدئو',
        blank=True,
        help_text='لینک صفحه ویدئو در آپارات یا هر سرویس دیگر.',
    )
    duration = models.CharField(
        'مدت زمان',
        max_length=12,
        blank=True,
        help_text='مثال: ۰۵:۴۰',
    )
    quality = models.CharField(
        'کیفیت',
        max_length=20,
        blank=True,
        default='۱۰۸۰p',
    )

    class Meta:
        verbose_name = 'ویدئو'
        verbose_name_plural = 'ویدئوها'
        ordering = ('order', '-published_at', '-id')

    def __str__(self):
        return self.title


class Magazine(PublishableModel):
    """نشریات و گاهنامه‌های مکتوب."""

    kind = 'magazine'

    title = models.CharField('عنوان نشریه', max_length=200)
    issue_label = models.CharField(
        'شماره / دوره',
        max_length=80,
        blank=True,
        help_text='مثال: شماره پاییز ۱۴۰۳',
    )
    summary = models.TextField('توضیح کوتاه')
    page_count = models.PositiveIntegerField('تعداد صفحات', null=True, blank=True)
    pdf_file = models.FileField(
        'فایل PDF (آپلود)',
        upload_to='magazines/',
        blank=True,
        null=True,
    )
    pdf_url = models.URLField(
        'یا لینک فایل PDF',
        blank=True,
        help_text='در صورتی که فایل را جای دیگری میزبانی می‌کنید.',
    )

    class Meta:
        verbose_name = 'نشریه'
        verbose_name_plural = 'نشریات'
        ordering = ('order', '-published_at', '-id')

    def __str__(self):
        return self.title

    @property
    def pdf_source(self):
        if self.pdf_file:
            return self.pdf_file.url
        return self.pdf_url

    @property
    def page_label(self):
        if not self.page_count:
            return 'PDF'
        return f'{to_persian_digits(self.page_count)} صفحه | PDF'


class NewsItem(PublishableModel):
    """اخبار، اطلاعیه‌ها و رویدادها."""

    title = models.CharField('عنوان خبر', max_length=200)
    category = models.CharField('دسته‌بندی', max_length=80, default='اطلاعیه رسمی')
    summary = models.TextField('خلاصه خبر')
    highlight = models.CharField(
        'متن شاخص (پایین کارت)',
        max_length=80,
        blank=True,
        help_text='مثال: مهلت تا ۳۰ مهر',
    )
    action_label = models.CharField(
        'متن دکمه / لینک',
        max_length=60,
        blank=True,
        default='اطلاعات بیشتر',
    )
    action_url = models.URLField(
        'آدرس دکمه / لینک',
        blank=True,
        help_text='می‌توانید به بخشی از سایت هم لینک بدهید. مثال: /#team',
    )

    class Meta:
        verbose_name = 'خبر / اطلاعیه'
        verbose_name_plural = 'اخبار و اطلاعیه‌ها'
        ordering = ('order', '-published_at', '-id')

    def __str__(self):
        return self.title


class AdvocacyCase(PublishableModel):
    """پرونده‌های مطالبه‌گری در حال پیگیری."""

    ACCENT_AMBER = 'amber'
    ACCENT_GREEN = 'green'
    ACCENT_BLUE = 'blue'
    ACCENT_GRAY = 'gray'
    ACCENT_CHOICES = [
        (ACCENT_AMBER, 'نارنجی (در حال پیگیری)'),
        (ACCENT_GREEN, 'سبز (به نتیجه رسیده)'),
        (ACCENT_BLUE, 'آبی (در حال بررسی)'),
        (ACCENT_GRAY, 'خاکستری (آرشیو)'),
    ]

    code = models.CharField(
        'کد پرونده',
        max_length=20,
        blank=True,
        help_text='مثال: H-104 (اگر خالی بماند خودکار ساخته می‌شود).',
    )
    status_label = models.CharField(
        'وضعیت پرونده',
        max_length=80,
        default='در حال پیگیری',
    )
    accent = models.CharField(
        'رنگ وضعیت',
        max_length=10,
        choices=ACCENT_CHOICES,
        default=ACCENT_AMBER,
    )
    title = models.CharField('عنوان مطالبه', max_length=200)
    description = models.TextField('شرح اقدامات انجام‌شده')
    next_step = models.CharField(
        'گام بعدی',
        max_length=150,
        blank=True,
        help_text='مثال: انتشار پاسخ کتبی مسئولین',
    )
    progress = models.PositiveSmallIntegerField(
        'درصد پیشرفت',
        default=0,
        validators=[MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = 'پرونده مطالبه‌گری'
        verbose_name_plural = 'پرونده‌های مطالبه‌گری'
        ordering = ('order', '-published_at', '-id')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating and not self.code:
            self.code = f'H-{100 + self.pk}'
            super().save(update_fields=['code'])

    @property
    def progress_label(self):
        return f'{to_persian_digits(self.progress)}٪'


class AdvocacySubmission(models.Model):
    """مطالباتی که بازدیدکنندگان از فرم سایت ارسال می‌کنند."""

    institution = models.CharField('نهاد مربوطه', max_length=150)
    subject = models.CharField('موضوع مطالبه', max_length=200)
    description = models.TextField('شرح مسئله')
    contact = models.CharField('راه ارتباطی', max_length=120, blank=True)
    tracking_code = models.CharField('کد رهگیری', max_length=20, unique=True, blank=True)
    is_reviewed = models.BooleanField('بررسی شد', default=False)
    created_at = models.DateTimeField('تاریخ ارسال', auto_now_add=True)

    class Meta:
        verbose_name = 'مطالبه دریافتی'
        verbose_name_plural = 'مطالبات دریافتی'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.subject} ({self.tracking_code})'

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)
        if creating and not self.tracking_code:
            self.tracking_code = f'H-{1000 + self.pk}'
            super().save(update_fields=['tracking_code'])


class TeamMember(PublishableModel):
    """اعضای کادر رسانه‌ای همسو."""

    name = models.CharField('عنوان سمت / نام', max_length=120)
    unit = models.CharField('واحد سازمانی', max_length=120, blank=True)
    description = models.TextField('شرح وظایف')
    icon = models.CharField(
        'آیکون',
        max_length=60,
        default='fa-user-tie',
        help_text='نام آیکون FontAwesome، مثال: fa-microphone-alt',
    )
    photo = models.ImageField(
        'عکس (اختیاری)',
        upload_to='team/',
        blank=True,
        null=True,
        help_text='در صورت خالی بودن، آیکون نمایش داده می‌شود.',
    )

    class Meta:
        verbose_name = 'عضو تیم'
        verbose_name_plural = 'اعضای تیم'
        ordering = ('order', 'id')

    def __str__(self):
        return self.name


class StatementPrinciple(PublishableModel):
    """بندهای بیانیه گام اول."""

    title = models.CharField('عنوان اصل', max_length=150)
    body = models.TextField('متن اصل')

    class Meta:
        verbose_name = 'اصل بیانیه'
        verbose_name_plural = 'اصول بیانیه گام اول'
        ordering = ('order', 'id')

    def __str__(self):
        return self.title


class UniversityFeature(PublishableModel):
    """سرفصل‌های فعالیت همسو در دانشگاه."""

    title = models.CharField('عنوان', max_length=120)
    body = models.TextField('توضیح')
    icon = models.CharField(
        'آیکون',
        max_length=60,
        default='fa-chalkboard-teacher',
        help_text='نام آیکون FontAwesome، مثال: fa-lightbulb',
    )

    class Meta:
        verbose_name = 'فعالیت دانشگاهی'
        verbose_name_plural = 'فعالیت‌های دانشگاهی'
        ordering = ('order', 'id')

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """تنظیمات و متن‌های عمومی سایت (تک‌نمونه‌ای)."""

    site_name = models.CharField('نام رسانه', max_length=80, default='رسانه همسو')
    tagline = models.CharField(
        'شعار زیر لوگو',
        max_length=150,
        default='رسانه‌ای از دل مردم، برای مردم',
    )
    hashtag = models.CharField('هشتگ', max_length=60, default='#باید_برخاست')

    about_title = models.CharField(
        'عنوان کارت معرفی',
        max_length=150,
        default='رزومه و هویت رسانه همسو',
    )
    about_text = models.TextField(
        'متن معرفی',
        default=(
            'گروه رسانه‌ای «همسو» با تکیه بر آرمان‌های اصیل و بیانیه گام دوم، '
            'رسانه‌ای متعهد و پویا از دل دانشگاه و مردم است که با تولید محتوای '
            'چندرسانه‌ای نوین و مطالبه‌گری شفاف، بستری برای شکوفایی، آگاهی‌بخشی '
            'و توسعه اجتماعی فراهم می‌سازد.'
        ),
    )
    stat_one_value = models.CharField('آمار ۱ - عدد', max_length=20, default='+۲۵')
    stat_one_label = models.CharField(
        'آمار ۱ - توضیح',
        max_length=80,
        default='پادکست و رسانه صوتی',
    )
    stat_two_value = models.CharField('آمار ۲ - عدد', max_length=20, default='+۱۵')
    stat_two_label = models.CharField(
        'آمار ۲ - توضیح',
        max_length=80,
        default='شماره نشریه مستقل',
    )

    statement_title = models.CharField(
        'بیانیه - عنوان',
        max_length=200,
        default='«#باید_برخاست؛ رسالتی برای تغییر مثبت»',
    )
    statement_subtitle = models.CharField(
        'بیانیه - برچسب بالای عنوان',
        max_length=80,
        default='سند بنیادین تأسیس',
    )
    statement_intro = models.TextField(
        'بیانیه - مقدمه',
        default=(
            'بسم‌الله‌الرحمن‌الرحیم. گروه رسانه‌ای و تشکل اداری «همسو» با هدف تحقق '
            'شعار «رسانه‌ای از دل مردم، برای مردم» شکل گرفته است. ما باور داریم که '
            'پیشرفت، عدالت و تعالی جامعه در گرو آگاهی، شفافیت و جسارت در پیگیری حق است.'
        ),
    )

    university_title = models.CharField(
        'دانشگاه - عنوان',
        max_length=200,
        default='پیوند علم، عمل و مسئولیت اجتماعی',
    )
    university_intro = models.TextField(
        'دانشگاه - مقدمه',
        default=(
            'دانشگاه صرفاً محلی برای آموزش تئوری نیست؛ بلکه مبدأ تمام تحولات جامعه و '
            'کانون تربیت مدیران آینده کشور است. رسانه همسو در بستر دانشگاه به عنوان '
            'پل ارتباطی میان بدنه پویای دانشجویی، اعضای هیئت علمی و مدیران اجرایی عمل '
            'می‌کند تا دغدغه‌ها به راه‌حل‌های علمی و عملیاتی تبدیل گردند.'
        ),
    )

    contact_email = models.EmailField('ایمیل ارتباطی', blank=True)
    contact_phone = models.CharField('شماره تماس', max_length=40, blank=True)
    link_ita = models.URLField('لینک ایتا', blank=True)
    link_bale = models.URLField('لینک بله', blank=True)
    link_aparat = models.URLField('لینک آپارات', blank=True)
    link_instagram = models.URLField('لینک اینستاگرام', blank=True)

    footer_text = models.CharField(
        'متن پاورقی',
        max_length=200,
        default='رسانه‌ای از دل مردم، برای مردم | #باید_برخاست',
    )
    copyright_text = models.CharField(
        'متن حق نشر',
        max_length=200,
        default='تمامی حقوق مادی و معنوی متعلق به گروه رسانه‌ای همسو می‌باشد.',
    )
    updated_at = models.DateTimeField('آخرین ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.site_name

    @classmethod
    def load(cls):
        """نمونه‌ی تنظیمات را برمی‌گرداند؛ در صورت خالی بودن، مقادیر پیش‌فرض."""
        return cls.objects.first() or cls()
