"""پنل مدیریت اختصاصی رسانه همسو.

تنها کاربری که پرچم «سوپر یوزر» دارد می‌تواند وارد این پنل شود.
ساخت کاربر سوپر یوزر با دستور زیر انجام می‌شود:

    python manage.py createsuperuser

سپس از آدرس /admin/ وارد شوید.
"""

from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import (
    AdvocacyCase,
    AdvocacySubmission,
    Magazine,
    NewsItem,
    Podcast,
    SiteSettings,
    StatementPrinciple,
    TeamMember,
    UniversityFeature,
    Video,
)


class SuperuserLoginForm(AuthenticationForm):
    """فرم ورود پنل؛ فقط سوپر یوزرها مجاز هستند."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise ValidationError(
                'ورود به پنل مدیریت فقط برای کاربر سوپر یوزر مجاز است.',
                code='not_superuser',
            )


class HamsooAdminSite(admin.AdminSite):
    site_header = 'پنل مدیریت رسانه همسو'
    site_title = 'مدیریت همسو'
    index_title = 'مدیریت محتوای سایت'
    login_form = SuperuserLoginForm

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


admin_site = HamsooAdminSite(name='admin')


class PublishableAdmin(admin.ModelAdmin):
    """تنظیمات مشترک مدل‌های محتوایی."""

    list_filter = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True
    list_per_page = 25

    @admin.display(description='تاریخ', ordering='published_at')
    def date_column(self, obj):
        return obj.display_date


@admin.register(Podcast, site=admin_site)
class PodcastAdmin(PublishableAdmin):
    list_display = ('title', 'episode_label', 'kind_label', 'duration', 'date_column', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'summary', 'kind_label')
    fieldsets = (
        ('اطلاعات قسمت', {'fields': ('title', 'kind_label', 'episode_number', 'summary')}),
        ('فایل صوتی', {
            'fields': ('audio_file', 'audio_url', 'duration'),
            'description': 'یکی از دو مورد «فایل صوتی» یا «لینک فایل صوتی» را پر کنید.',
        }),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Video, site=admin_site)
class VideoAdmin(PublishableAdmin):
    list_display = ('title', 'category_label', 'duration', 'quality', 'date_column', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'summary', 'category_label')
    fieldsets = (
        ('اطلاعات ویدئو', {'fields': ('title', 'category_label', 'summary')}),
        ('فایل و لینک', {
            'fields': ('thumbnail', 'video_url', 'duration', 'quality'),
            'description': 'لینک ویدئو می‌تواند صفحه آپارات یا هر سرویس میزبانی دیگر باشد.',
        }),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Magazine, site=admin_site)
class MagazineAdmin(PublishableAdmin):
    list_display = ('title', 'issue_label', 'page_count', 'date_column', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'summary', 'issue_label')
    fieldsets = (
        ('اطلاعات نشریه', {'fields': ('title', 'issue_label', 'summary', 'page_count')}),
        ('فایل PDF', {
            'fields': ('pdf_file', 'pdf_url'),
            'description': 'یکی از دو مورد «فایل PDF» یا «لینک فایل PDF» را پر کنید.',
        }),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(NewsItem, site=admin_site)
class NewsItemAdmin(PublishableAdmin):
    list_display = ('title', 'category', 'date_column', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'summary', 'category')
    fieldsets = (
        ('متن خبر', {'fields': ('title', 'category', 'summary')}),
        ('دکمه و لینک پایین کارت', {'fields': ('highlight', 'action_label', 'action_url')}),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(AdvocacyCase, site=admin_site)
class AdvocacyCaseAdmin(PublishableAdmin):
    list_display = ('title', 'code', 'status_label', 'accent', 'progress', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published', 'accent')
    search_fields = ('title', 'description', 'code', 'status_label')
    fieldsets = (
        ('اطلاعات پرونده', {
            'fields': ('code', 'status_label', 'accent', 'title', 'description', 'next_step', 'progress'),
        }),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(AdvocacySubmission, site=admin_site)
class AdvocacySubmissionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'institution', 'contact', 'tracking_code', 'is_reviewed', 'created_at')
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('subject', 'institution', 'description', 'tracking_code')
    readonly_fields = ('institution', 'subject', 'description', 'contact', 'tracking_code', 'created_at')
    fields = ('tracking_code', 'institution', 'contact', 'subject', 'description', 'created_at', 'is_reviewed')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        # مطالبات فقط از فرم سایت ثبت می‌شوند.
        return False


@admin.register(TeamMember, site=admin_site)
class TeamMemberAdmin(PublishableAdmin):
    list_display = ('name', 'unit', 'icon', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('name', 'unit', 'description')
    fieldsets = (
        ('اطلاعات عضو', {'fields': ('name', 'unit', 'description', 'icon', 'photo')}),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(StatementPrinciple, site=admin_site)
class StatementPrincipleAdmin(PublishableAdmin):
    list_display = ('title', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'body')
    fieldsets = (
        ('متن اصل', {'fields': ('title', 'body')}),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(UniversityFeature, site=admin_site)
class UniversityFeatureAdmin(PublishableAdmin):
    list_display = ('title', 'icon', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    search_fields = ('title', 'body')
    fieldsets = (
        ('اطلاعات', {'fields': ('title', 'body', 'icon')}),
        ('انتشار', {'fields': ('is_published', 'order', 'published_at', 'date_label')}),
        ('زمان ثبت', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'updated_at')
    fieldsets = (
        ('هویت رسانه', {'fields': ('site_name', 'tagline', 'hashtag')}),
        ('کارت معرفی صفحه اصلی', {
            'fields': ('about_title', 'about_text', 'stat_one_value', 'stat_one_label', 'stat_two_value', 'stat_two_label'),
        }),
        ('بیانیه گام اول', {'fields': ('statement_subtitle', 'statement_title', 'statement_intro')}),
        ('همسو در دانشگاه', {'fields': ('university_title', 'university_intro')}),
        ('راه‌های ارتباطی', {'fields': ('contact_email', 'contact_phone', 'link_ita', 'link_bale', 'link_aparat', 'link_instagram')}),
        ('پاورقی', {'fields': ('footer_text', 'copyright_text')}),
    )
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # تنظیمات سایت فقط یک نمونه دارد.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
