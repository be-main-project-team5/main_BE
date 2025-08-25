#!/bin/bash
set -e


# 데이터베이스 마이그레이션
echo "Applying database migrations..."
python manage.py migrate --noinput

# 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 3 -b 0.0.0.0:8000
