"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve

from core.admin import admin_site

urlpatterns = [
    # پنل مدیریت (فقط کاربر سوپر یوزر)
    path('admin/', admin_site.urls),
    # سایت اصلی
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # در حالت production فایل‌های آپلودی (صدا/ویدئو/PDF) با جنگو سرو می‌شوند؛
    # در صورت افزایش ترافیک می‌توان در آینده media را به فضای ابری منتقل کرد.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
