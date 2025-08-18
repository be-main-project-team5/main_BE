from django.db import models

from apps.groups.models import Group
from apps.idols.models import Idol
from apps.users.models import CustomUser


# IdolBookmark 모델 정의
class IdolBookmark(models.Model):
    # 북마크한 사용자 (CustomUser 모델의 ForeignKey)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # 사용자가 삭제되면 북마크도 삭제
        null=False,
        blank=False,
        related_name="idol_bookmarks",  # 역참조 이름 설정
    )
    # 북마크된 아이돌 (idols 테이블의 ForeignKey)
    idol = models.ForeignKey(
        Idol,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="bookmarked_by_users",
    )

    # 북마크 생성 일시를 자동으로 기록합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "bookmarks_idolbookmark"
        # Django 관리자 페이지에 표시될 이름을 설정합니다。
        verbose_name = "아이돌 즐겨찾기"
        verbose_name_plural = "아이돌 즐겨찾기"
        # user와 idol 조합이 고유해야 합니다. (한 사용자가 같은 아이돌을 두 번 북마크할 수 없음)
        unique_together = ("user", "idol")

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용자 이메일과 아이돌 이름을 반환합니다.
        return f"{self.user.email} - 아이돌: {self.idol.name}"


# GroupBookmark 모델 정의
class GroupBookmark(models.Model):
    # 북마크한 사용자 (CustomUser 모델의 ForeignKey)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # 사용자가 삭제되면 북마크도 삭제
        null=False,
        blank=False,
        related_name="group_bookmarks",  # 역참조 이름 설정
    )
    # 북마크된 그룹 (groups 테이블의 ForeignKey)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="bookmarked_by_users",
    )

    # 북마크 생성 일시를 자동으로 기록합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "bookmarks_groupbookmark"
        # Django 관리자 페이지에 표시될 이름을 설정합니다。
        verbose_name = "그룹 즐겨찾기"
        verbose_name_plural = "그룹 즐겨찾기"
        # user와 group 조합이 고유해야 합니다. (한 사용자가 같은 그룹을 두 번 북마크할 수 없음)
        unique_together = ("user", "group")

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용자 이메일과 그룹 이름을 반환합니다.
        return f"{self.user.email} - 그룹: {self.group.name}"
