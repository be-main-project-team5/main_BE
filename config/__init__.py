from .celery import app as celery_app

__all__ = ("celery_app",) #장고가 실행될 때 셀러리도 실행
