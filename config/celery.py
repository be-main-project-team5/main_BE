import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


app = Celery("config")  # Celery 앱 생성
app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)  # settings.py에서 CELERY관련 설정 불러옴
app.autodiscover_tasks()  # 각 앱의 tasks.py 탐색


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
