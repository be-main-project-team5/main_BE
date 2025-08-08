from django.db import models
from django.conf import settings
from apps.idols.models import Idol
from apps.groups.models import Group

class IdolSchedule(models.Model):
    idol = models.ForeignKey(Idol, on_delete=models.CASCADE, related_name="schedules")
    manager = models.ForeignKey(  # 작성자
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="written_schedules",
        help_text="이 스케줄을 작성한 아이돌 매니저",
    )
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=5000)
    description = models.CharField(max_length=5000)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.idol.name} - {self.title}"

    class Meta:
        verbose_name = "아이돌 스케줄"
        verbose_name_plural = "아이돌 스케줄"


class GroupSchedule(models.Model):
    """
    그룹 스케줄 모델
    """

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="schedules",
        help_text="스케줄이 속한 그룹",
    )
    author = models.ForeignKey(  # 작성자
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="written_group_schedules",
        help_text="이 스케줄을 작성한 사용자",
    )
    start_time = models.DateTimeField(help_text="시작 시간")
    end_time = models.DateTimeField(help_text="종료 시간")
    location = models.CharField(max_length=5000, help_text="장소")
    description = models.CharField(max_length=5000, help_text="설명")
    is_public = models.BooleanField(default=True, help_text="공개 여부")
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 일시")

    class Meta:
        verbose_name = "그룹 스케줄"
        verbose_name_plural = "그룹 스케줄"

    def __str__(self):
        return f"{self.group.name} - {self.description[:20]}"


class UserSchedule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="my_schedules",
    )
    # 아이돌 스케줄 또는 그룹 스케줄 중 하나를 참조
    idol_schedule = models.ForeignKey(
        IdolSchedule,
        on_delete=models.CASCADE,
        null=True,  # 둘 중 하나는 null이 될 수 있음
        blank=True,
        related_name="user_added_schedules",
    )
    group_schedule = models.ForeignKey(
        GroupSchedule,
        on_delete=models.CASCADE,
        null=True, # 둘 중 하나는 null이 될 수 있음
        blank=True,
        related_name='user_added_schedules'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_schedules"
        verbose_name = "사용자 스케줄"
        verbose_name_plural = "사용자 스케줄"
        # 한 사용자가 동일한 아이돌 스케줄 또는 그룹 스케줄을 두 번 추가할 수 없도록
        unique_together = (("user", "idol_schedule"), ("user", "group_schedule"))

    def __str__(self):
        if self.idol_schedule:
            return (
                f"{self.user.email} - 아이돌 스케줄: {self.idol_schedule.description}"
            )
        elif self.group_schedule:
            return f"{self.user.email} - 그룹 스케줄: {self.group_schedule.description}"
        return f"{self.user.email} - 스케줄 없음"