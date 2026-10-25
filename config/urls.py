"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from core.admin import admin_site

urlpatterns = [
    # پنل مدیریت (فقط کاربر سوپر یوزر)
    path('admin/', admin_site.urls),
    # سایت اصلی
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
