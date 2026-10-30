# ---------------------------------------------------------------------------
# ایمیج تولیدی سایت رسانه همسو (Django + Gunicorn + WhiteNoise)
#
# ساخت محلی:
#   docker build -t hamsoo .
# اجرا:
#   docker run -p 8000:8000 -v hamsoo_data:/app/data hamsoo
# ---------------------------------------------------------------------------

# تصویر پایه؛ در صورت مسدود بودن Docker Hub می‌توانید با build arg
# آینه‌ی داخلی را بدهید: --build-arg PYTHON_IMAGE=docker.arvancloud.ir/python:3.13-slim
ARG PYTHON_IMAGE=python:3.13-slim
FROM ${PYTHON_IMAGE}

# آینه‌ی PyPI؛ برای شبکه‌هایی که pypi.org در دسترس نیست.
# در کولیفای می‌توانید در بخش Build Arguments مقدار PIP_INDEX_URL را تغییر دهید.
ARG PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=${PIP_INDEX_URL} \
    DJANGO_DEBUG=False \
    DJANGO_DATA_DIR=/app/data \
    PORT=8000

WORKDIR /app

# نصب وابستگی‌ها قبل از کپی کد، برای استفاده‌ی بهتر از کش لایه‌ها
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# آماده‌سازی پوشه‌های ماندگار، استاتیک‌ها و اسکریپت اجرا
RUN mkdir -p /app/data/media /app/staticfiles \
    && python manage.py collectstatic --noinput \
    && chmod +x /app/entrypoint.sh

EXPOSE 8000

# بررسی سلامت کانتینر (Coolify هم می‌تواند از مسیر /healthz/ استفاده کند)
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz/', timeout=4).status == 200 else 1)"

ENTRYPOINT ["/app/entrypoint.sh"]
