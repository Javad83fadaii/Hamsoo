"""پر کردن دیتابیس با محتوای نمونه (اختیاری).

این دستور فقط جدول‌هایی را پر می‌کند که خالی هستند، بنابراین محتوای
وارد شده از پنل مدیریت را پاک نمی‌کند.

    python manage.py seed_demo
"""

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    AdvocacyCase,
    Magazine,
    NewsItem,
    Podcast,
    SiteSettings,
    StatementPrinciple,
    TeamMember,
    UniversityFeature,
    Video,
)


class Command(BaseCommand):
    help = 'ثبت محتوای نمونه برای بخش‌های مختلف سایت (فقط جدول‌های خالی)'

    def handle(self, *args, **options):
        created = []

        if not SiteSettings.objects.exists():
            SiteSettings.objects.create()
            created.append('تنظیمات سایت')

        if not Podcast.objects.exists():
            Podcast.objects.bulk_create([
                Podcast(
                    title='صدای مطالبه: دانشگاه در تراز تمدن',
                    kind_label='پادکست صوتی',
                    episode_number=12,
                    summary=(
                        'گفتگوی بی‌پرده با نمایندگان تشکل‌های دانشجویی در خصوص جایگاه '
                        'دانشجو در تصمیم‌گیری‌های اداری.'
                    ),
                    duration='۲۱:۴۰',
                    order=1,
                ),
                Podcast(
                    title='شفافیت؛ کلید توسعه اداری',
                    kind_label='پادکست گفتگومحور',
                    episode_number=11,
                    summary=(
                        'بررسی شیوه‌های پاسخگویی مسئولان و مکانیزم‌های مطالبه‌گری سالم '
                        'در نهادهای دولتی.'
                    ),
                    duration='۱۸:۵۰',
                    order=2,
                ),
            ])
            created.append('پادکست‌ها')

        if not Video.objects.exists():
            Video.objects.bulk_create([
                Video(
                    title='روایت امید و محرومیت‌زدایی',
                    category_label='مستند گزارش میدانی',
                    summary=(
                        'گزارش تصویری از اردوی جهادی و اداری همسو در مناطق حاشیه شهر '
                        'با شعار باید برخاست.'
                    ),
                    duration='۰۵:۴۰',
                    quality='۱۰۸۰p',
                    order=1,
                ),
                Video(
                    title='هم‌افزایی جوانان در مدیریت',
                    category_label='گفتگوی اختصاصی',
                    summary=(
                        'میزگرد با اساتید مدیریت پیرامون به‌کارگیری ظرفیت تشکل‌های نخبگانی '
                        'در تصمیم‌گیری‌ها.'
                    ),
                    duration='۱۲:۱۵',
                    quality='۷۲۰p',
                    order=2,
                ),
            ])
            created.append('ویدئوها')

        if not Magazine.objects.exists():
            Magazine.objects.bulk_create([
                Magazine(
                    title='گاهنامه تخصصی «همسو» - شماره هشتم',
                    issue_label='شماره پائیز ۱۴۰۳',
                    summary=(
                        'پرونده ویژه عدالت آموزشی، تحلیل ساختار تصمیم‌گیری اداری و '
                        'مصاحبه با صاحب‌نظران عرصه رسانه.'
                    ),
                    page_count=36,
                    order=1,
                ),
                Magazine(
                    title='ویژه‌نامه گام دوم؛ جوانان و رسالت‌ها',
                    issue_label='شماره تابستان ۱۴۰۳',
                    summary=(
                        'بررسی بندهای مهم بیانیه گام دوم و تبدیل آن به پروژه‌های عملیاتی '
                        'اجرایی در فضای دانشگاهی.'
                    ),
                    page_count=28,
                    order=2,
                ),
            ])
            created.append('نشریات')

        if not NewsItem.objects.exists():
            NewsItem.objects.bulk_create([
                NewsItem(
                    title='فراخوان جذب گوینده، تدوین‌گر و طراح گرافیک',
                    category='اطلاعیه رسمی',
                    published_at=datetime.date(2024, 10, 5),
                    date_label='۱۴ مهر ۱۴۰۳',
                    summary=(
                        'گروه رسانه‌ای همسو از میان دانشجویان و جوانان علاقه‌مند به کار '
                        'رسانه‌ای، خبرنگاری و تدوین دعوت به همکاری می‌نماید.'
                    ),
                    highlight='مهلت تا ۳۰ مهر',
                    action_label='اطلاعات بیشتر',
                    action_url='/#team',
                    order=1,
                ),
                NewsItem(
                    title='برگزاری کارگاه «روزنامه‌نگاری تحقیقی و مطالبه‌گری اداری»',
                    category='رویداد حضوری',
                    published_at=datetime.date(2024, 9, 23),
                    date_label='۲ مهر ۱۴۰۳',
                    summary=(
                        'این کارگاه با حضور اساتید برجسته علوم ارتباطات و با هدف '
                        'توانمندسازی دانشجویان در تالار همایش دانشگاه برگزار شد.'
                    ),
                    highlight='همراه با گواهی حضور',
                    action_label='مشاهده گزارش',
                    order=2,
                ),
                NewsItem(
                    title='انتشار گزارش ۶ ماهه فعالیت‌های چندرسانه‌ای همسو',
                    category='گزارش عملکرد',
                    published_at=datetime.date(2024, 9, 15),
                    date_label='۲۵ شهریور ۱۴۰۳',
                    summary=(
                        'در این گزارش، آمار بیش از ۱۰۰ ساعت برنامه صوتی و تصویری، ۵ شماره '
                        'نشریه و نتایج پرونده‌های مطالبه‌گری ارائه شده است.'
                    ),
                    highlight='فایل PDF تفصیلی',
                    action_label='دریافت فایل',
                    order=3,
                ),
            ])
            created.append('اخبار')

        if not AdvocacyCase.objects.exists():
            AdvocacyCase.objects.bulk_create([
                AdvocacyCase(
                    code='H-104',
                    status_label='در حال پیگیری میدانی',
                    accent=AdvocacyCase.ACCENT_AMBER,
                    title='بهبود شرایط اسکان و امکانات رفاهی خوابگاه‌های دانشگاهی',
                    description=(
                        'تشکیل جلسه مشترک با مسئولین امور رفاهی و تنظیم نامه سرگشاده جهت '
                        'تخصیص فوری اعتبارات نوسازی.'
                    ),
                    next_step='انتشار پاسخ کتبی مسئولین',
                    progress=70,
                    order=1,
                ),
                AdvocacyCase(
                    code='H-098',
                    status_label='به نتیجه رسیده',
                    accent=AdvocacyCase.ACCENT_GREEN,
                    title='شفاف‌سازی فرآیند تخصیص بودجه فرهنگی دانشگاه',
                    description=(
                        'با تلاش رسانه‌ای و تدوین مستند گزارشی، جدول نهایی بودجه به تفکیک '
                        'فعالیت کانون‌ها برای اولین بار علنی شد.'
                    ),
                    next_step='گزارش در وبسایت درج گردید',
                    progress=100,
                    order=2,
                ),
                AdvocacyCase(
                    code='H-109',
                    status_label='در مرحله جمع‌آوری اسناد',
                    accent=AdvocacyCase.ACCENT_BLUE,
                    title='نظارت بر فرآیند برون‌سپاری خدمات اداری',
                    description=(
                        'بررسی شکایات واصله پیرامون کیفیت عملکرد پیمانکاران طرف قرارداد و '
                        'بررسی حقوق کارگران خدماتی.'
                    ),
                    next_step='ارسال استعلام حقوقی',
                    progress=30,
                    order=3,
                ),
            ])
            created.append('پرونده‌های مطالبه‌گری')

        if not TeamMember.objects.exists():
            TeamMember.objects.bulk_create([
                TeamMember(
                    name='دبیر و سرپرست گروه',
                    unit='شورای مرکزی',
                    description='هدایت سیاست‌های کلی، هماهنگی بخش‌های اداری و نظارت بر راهبردها',
                    icon='fa-user-tie',
                    order=1,
                ),
                TeamMember(
                    name='سردبیر نشریه و محتوا',
                    unit='واحد تولید متن',
                    description='نگارش مقالات تحلیلی، ویراستاری نشریه و تدوین سناریوی پادکست‌ها',
                    icon='fa-pen-fancy',
                    order=2,
                ),
                TeamMember(
                    name='مدیر تولید چندرسانه‌ای',
                    unit='واحد پادکست و ویدئو',
                    description='ضبط و میکس پادکست‌های صوتی، تدوین ویدئوکلیپ‌ها و مصاحبه‌ها',
                    icon='fa-microphone-alt',
                    order=3,
                ),
                TeamMember(
                    name='مسئول واحد مطالبه‌گری',
                    unit='حقوقی و ارتباطات',
                    description='بررسی پرونده‌های صنفی، مکاتبات رسمی با نهادها و پیگیری بازخوردها',
                    icon='fa-balance-scale',
                    order=4,
                ),
            ])
            created.append('اعضای تیم')

        if not StatementPrinciple.objects.exists():
            StatementPrinciple.objects.bulk_create([
                StatementPrinciple(
                    title='اصل اول: استقلال و صداقت در روایت',
                    body=(
                        'همسو وابسته به هیچ جناح سیاسی، حزب یا فرد خاصی نبوده و تنها تعهد ما، '
                        'حقیقت، منافع مردم و اعتلای میهن عزیزمان ایران است.'
                    ),
                    order=1,
                ),
                StatementPrinciple(
                    title='اصل دوم: مطالبه‌گری اخلاق‌مدار',
                    body=(
                        'مطالبه‌گری از نگاه ما به معنای تخریب نیست؛ بلکه نقد سازنده، ارائه '
                        'مستند راهکار علمی و پیگیری خستگی‌ناپذیر تا اصلاح امور است.'
                    ),
                    order=2,
                ),
                StatementPrinciple(
                    title='اصل سوم: میدان دادن به جوانان و ظرفیت‌های دانشگاهی',
                    body=(
                        'بسترسازی برای تجلی استعدادهای دانشجویی، تولید محتوای وزین چندرسانه‌ای '
                        'و پایبندی به آرمان‌های انقلاب اسلامی و بیانیه گام دوم.'
                    ),
                    order=3,
                ),
            ])
            created.append('اصول بیانیه')

        if not UniversityFeature.objects.exists():
            UniversityFeature.objects.bulk_create([
                UniversityFeature(
                    title='میزگردهای تخصصی',
                    body=(
                        'برگزاری سلسله جلسات تحلیل سیاست‌گذاری‌های عمومی با حضور اساتید و '
                        'مسئولین اداری.'
                    ),
                    icon='fa-chalkboard-teacher',
                    order=1,
                ),
                UniversityFeature(
                    title='شورای هماهنگی صنفی',
                    body=(
                        'همراهی مستمر با کانون‌ها و تشکل‌ها جهت انتقال شفاف مطالبات دانشجویان '
                        'به مدیریت دانشگاه.'
                    ),
                    icon='fa-hands-helping',
                    order=2,
                ),
                UniversityFeature(
                    title='اتاق ایده‌پردازی نخبگان',
                    body=(
                        'جمع‌آوری و تدوین طرح‌های پیشنهادی دانشجویان نخبه برای حل معضلات '
                        'اداری و اجرایی کشور.'
                    ),
                    icon='fa-lightbulb',
                    order=3,
                ),
            ])
            created.append('فعالیت‌های دانشگاهی')

        if created:
            self.stdout.write(self.style.SUCCESS('محتوای نمونه ثبت شد: ' + '، '.join(created)))
        else:
            self.stdout.write(self.style.WARNING('همه‌ی بخش‌ها از قبل محتوا داشتند؛ چیزی تغییر نکرد.'))

        self.stdout.write(f'تاریخ اجرا: {timezone.localdate()}')
