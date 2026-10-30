#!/usr/bin/env sh
set -e

DATA_DIR="${DJANGO_DATA_DIR:-/app/data}"
mkdir -p "$DATA_DIR/media"

echo "==> [hamsoo] applying database migrations"
python manage.py migrate --noinput

echo "==> [hamsoo] collecting static files"
python manage.py collectstatic --noinput

# ساخت کاربر سوپر یوزر اولیه از روی متغیرهای محیطی (در صورت نبودِ کاربر)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "==> [hamsoo] ensuring superuser '$DJANGO_SUPERUSER_USERNAME' exists"
  python manage.py createsuperuser --noinput 2>/dev/null || true
fi

# بارگذاری محتوای نمونه (فقط برای اولین اجرا؛ روی جدول‌های خالی کار می‌کند)
if [ "$DJANGO_SEED_DEMO" = "true" ] || [ "$DJANGO_SEED_DEMO" = "1" ]; then
  echo "==> [hamsoo] seeding demo content"
  python manage.py seed_demo || true
fi

echo "==> [hamsoo] starting gunicorn on 0.0.0.0:${PORT:-8000}"
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-120}" \
  --access-logfile - \
  --error-logfile -
