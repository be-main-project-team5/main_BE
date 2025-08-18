from django.db import models

from apps.schedules.models import GroupSchedule, IdolSchedule
from apps.users.models import CustomUser


class Alarm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="alarms"
    )

    # 연결된 스케줄 (둘 중 하나만 사용)
    idol_schedule = models.ForeignKey(
        IdolSchedule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alarms",
    )
    group_schedule = models.ForeignKey(
        GroupSchedule,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="alarms",
    )

    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(help_text="알람이 발송될 시간")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        base = self.idol_schedule or self.group_schedule
        return f"{self.user.nickname} - {self.message[:30]} ({base})"
