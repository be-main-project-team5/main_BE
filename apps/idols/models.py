from django.conf import settings
from django.db import models


class Idol(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 유저와 1대1이므로 원투원 필드 사용
    group = models.ForeignKey("groups.Group", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "아이돌"
        verbose_name_plural = "아이돌"


class IdolManager(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idol = models.ForeignKey(Idol, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "idol",
        )  # 같은 매니저가 같은 아이돌에 중복 등록되지 않도록
        verbose_name = "아이돌 매니저"
        verbose_name_plural = "아이돌 매니저"

    def __str__(self):
        return f"{self.user.nickname} → {self.idol.name}"



