from django.db import models

from apps.users.models import Image  # Image 모델 임포트


# ERD의 'groups' 테이블에 해당하는 Django 모델입니다.
# 이 모델은 아이돌 그룹의 핵심 정보를 정의하며, 데이터베이스 테이블과 직접적으로 매핑됩니다.
# 각 필드는 테이블의 컬럼을 나타내며, 데이터 유형과 제약 조건이 설정되어 있습니다.
# 이 모델은 'apps/groups/views.py'의 GroupViewSet과 'apps/groups/serializers.py'의 GroupSerializer에서 사용됩니다.
class Group(models.Model):
    # 그룹의 이름입니다.
    # CharField는 문자열을 저장하며, max_length는 최대 길이를 100자로 제한합니다.
    # unique=True는 이 필드의 값이 데이터베이스 전체에서 고유해야 함을 의미합니다.
    name = models.CharField(max_length=100, unique=True, help_text="그룹 이름")

    # 그룹의 데뷔 일자입니다.
    # DateField는 날짜(년, 월, 일)를 저장합니다.
    debut_date = models.DateField(help_text="데뷔 일자")

    # 그룹의 소속사 이름입니다.
    agency = models.CharField(max_length=100, help_text="소속사")

    # 그룹 로고 이미지 ID (Image 모델의 ForeignKey)
    logo_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,  # 이미지가 삭제되어도 그룹 정보는 유지
        null=True,  # 로고 이미지가 없을 수도 있습니다.
        blank=True,
        related_name="group_logos",  # 역참조 이름 설정
    )

    # 레코드가 처음 생성된 날짜와 시간입니다.
    # auto_now_add=True는 객체가 처음 생성될 때 현재 시간으로 자동 설정되도록 합니다.
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일시")

    # 레코드가 마지막으로 수정된 날짜와 시간입니다.
    # auto_now=True는 객체가 저장될 때마다 현재 시간으로 자동 업데이트되도록 합니다.
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 일시")

    class Meta:
        # Django 관리자 페이지에 표시될 이름을 설정합니다.
        verbose_name = "그룹"
        verbose_name_plural = "그룹들"

    # 객체를 문자열로 표현할 때 사용되는 메서드입니다.
    # Django 관리자 페이지나 디버깅 시 그룹의 이름을 쉽게 식별할 수 있도록 합니다.
    def __str__(self):
        return self.name


class GroupSchedule(models.Model):
    """
    그룹 스케줄 모델
    """
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='schedules',
        help_text="스케줄이 속한 그룹"
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
        verbose_name_plural = "그룹 스케줄들"

    def __str__(self):
        return f"{self.group.name} - {self.description[:20]}"
