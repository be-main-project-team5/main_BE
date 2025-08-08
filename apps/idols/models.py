from django.conf import settings
from django.db import models


class Idol(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 유저와 1대1이므로 원투원 필드 사용
    group = models.ForeignKey(
        "groups.Group", on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class IdolManager(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idol = models.ForeignKey(Idol, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "idol",
        )  # 같은 매니저가 같은 아이돌에 중복 등록되지 않도록

    def __str__(self):
        return f"{self.user.nickname} → {self.idol.name}"


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
