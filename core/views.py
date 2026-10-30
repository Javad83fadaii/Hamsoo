"""ویوهای سایت رسانه همسو."""

from django.contrib import messages
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AdvocacySubmissionForm
from .models import (
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


def index(request):
    """صفحه اصلی سایت؛ همه‌ی بخش‌ها با ناوبری سمت کلاینت نمایش داده می‌شوند."""
    if request.method == 'POST':
        form = AdvocacySubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            messages.success(
                request,
                f'مطالبه شما با موفقیت ثبت شد. کد رهگیری: {submission.tracking_code}',
            )
            return redirect(f'{reverse("core:index")}#advocacy')
        messages.error(request, 'ارسال مطالبه انجام نشد؛ لطفاً فیلدهای الزامی را کامل کنید.')
    else:
        form = AdvocacySubmissionForm()

    # پادکست‌ها، ویدئوها و نشریات در یک فهرست واحد و بر اساس ترتیب نمایش
    works = (
        list(Podcast.objects.published())
        + list(Video.objects.published())
        + list(Magazine.objects.published())
    )
    works.sort(key=lambda item: (item.order, -item.published_at.toordinal(), item.kind))

    context = {
        'site': SiteSettings.load(),
        'works': works,
        'cases': AdvocacyCase.objects.published(),
        'news_items': NewsItem.objects.published(),
        'team_members': TeamMember.objects.published(),
        'principles': StatementPrinciple.objects.published(),
        'features': UniversityFeature.objects.published(),
        'form': form,
    }
    return render(request, 'core/index.html', context)


def healthz(request):
    """بررسی سلامت سرویس: اتصال دیتابیس و آمادگی برنامه."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except Exception:
        return JsonResponse({'status': 'error', 'database': 'unavailable'}, status=503)
    return JsonResponse({'status': 'ok', 'database': 'ok'})
