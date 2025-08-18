from celery import shared_task
from django.utils import timezone

from .models import Alarm


@shared_task
def send_scheduled_alarms():
    """
    현재 시간 기준으로 알람 발송 시간이 된 Alarm들을 처리하는 Task
    """
    now = timezone.now()  # 현재 시각을 할당함. DB의 scheduled_time과 비교하기 위해서
    alarms_to_send = Alarm.objects.filter(scheduled_time__lte=now, is_read=False)

    for alarm in alarms_to_send:
        # 여기서 실제 발송 로직 (예: 푸시 알림, 이메일 등), 현재는 테스트용으로 콘솔로 확인함
        print(f"[알람 발송] {alarm.user.nickname}: {alarm.message}")

        # 발송 후 읽음 처리
        alarm.is_read = True
        alarm.save()
