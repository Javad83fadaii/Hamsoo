"""تست‌های پایه سایت و پنل مدیریت."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


class PublicSiteTests(TestCase):
    def test_home_page_renders_with_empty_database(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'همسو')

    def test_site_settings_values_are_used(self):
        SiteSettings.objects.create(site_name='رسانه تست', tagline='شعار تست')
        response = self.client.get(reverse('core:index'))
        self.assertContains(response, 'رسانه تست')
        self.assertContains(response, 'شعار تست')

    def test_only_published_content_is_visible(self):
        Podcast.objects.create(title='قسمت منتشر شده', summary='توضیح')
        Podcast.objects.create(title='قسمت مخفی', summary='توضیح', is_published=False)

        response = self.client.get(reverse('core:index'))

        self.assertContains(response, 'قسمت منتشر شده')
        self.assertNotContains(response, 'قسمت مخفی')

    def test_advocacy_form_creates_submission_with_tracking_code(self):
        response = self.client.post(reverse('core:index'), {
            'institution': 'معاونت دانشجویی',
            'subject': 'وضعیت خوابگاه‌ها',
            'description': 'شرح کامل مسئله',
            'contact': '۰۹۱۲۳۴۵۶۷۸۹',
        })

        self.assertEqual(response.status_code, 302)
        submission = AdvocacySubmission.objects.get()
        self.assertEqual(submission.subject, 'وضعیت خوابگاه‌ها')
        self.assertTrue(submission.tracking_code.startswith('H-'))

    def test_advocacy_form_rejects_empty_fields(self):
        self.client.post(reverse('core:index'), {
            'institution': '',
            'subject': '',
            'description': '',
        })

        self.assertEqual(AdvocacySubmission.objects.count(), 0)


class AdminAccessTests(TestCase):
    def test_superuser_can_open_admin_panel(self):
        user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='StrongPass!123',
        )
        self.client.force_login(user)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'پادکست‌ها')

    def test_staff_user_without_superuser_is_redirected(self):
        user = get_user_model().objects.create_user(
            username='staff', password='StrongPass!123', is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)

    def test_login_form_refuses_non_superuser(self):
        get_user_model().objects.create_user(
            username='staff', password='StrongPass!123', is_staff=True,
        )

        response = self.client.post(
            '/admin/login/?next=/admin/',
            {'username': 'staff', 'password': 'StrongPass!123'},
            follow=True,
        )

        self.assertContains(response, 'سوپر یوزر')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_every_admin_page_opens(self):
        user = get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='StrongPass!123',
        )
        self.client.force_login(user)

        models = (
            Podcast, Video, Magazine, NewsItem, AdvocacyCase,
            AdvocacySubmission, TeamMember, StatementPrinciple,
            UniversityFeature, SiteSettings,
        )

        for model in models:
            meta = model._meta
            changelist = reverse(f'admin:{meta.app_label}_{meta.model_name}_changelist')
            with self.subTest(page=meta.model_name, view='changelist'):
                self.assertEqual(self.client.get(changelist).status_code, 200)

            if model is AdvocacySubmission:
                # مطالبات دریافتی فقط قابل مشاهده و بررسی هستند
                continue

            add_page = reverse(f'admin:{meta.app_label}_{meta.model_name}_add')
            with self.subTest(page=meta.model_name, view='add'):
                self.assertEqual(self.client.get(add_page).status_code, 200)
