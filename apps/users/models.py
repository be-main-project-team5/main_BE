from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
import os


# Image 모델 정의 (프로필 이미지, 로고 이미지 등에 사용) / 나중에 common 앱으로 이동할 수 있다.
class Image(models.Model):
    # 실제 이미지 파일을 저장합니다.
    image_file = models.ImageField(upload_to='images/', null=True, blank=True)
    # 이미지 URL을 저장합니다. (image_file에서 자동 생성)
    url = models.CharField(max_length=2048, null=True, blank=True)
    # 파일 크기 (바이트 단위)를 저장합니다. (image_file에서 자동 생성)
    file_size = models.IntegerField(null=True, blank=True)
    # 이미지 생성 일시를 자동으로 기록합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "images"
        # Django 관리자 페이지에 표시될 이름을 설정합니다.
        verbose_name = "이미지"
        verbose_name_plural = "이미지들"

    def save(self, *args, **kwargs):
        if self.image_file:
            # 파일이 저장될 경로를 설정합니다.
            # default_storage.save는 파일 시스템에 파일을 저장하고 저장된 파일의 상대 경로를 반환합니다.
            # 이 경로를 MEDIA_URL과 결합하여 완전한 URL을 만듭니다.
            file_name = default_storage.save(os.path.join('images', self.image_file.name), self.image_file)
            self.url = settings.MEDIA_URL + file_name
            self.file_size = self.image_file.size
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 모델 인스턴스가 삭제될 때 연결된 파일도 삭제합니다.
        if self.image_file:
            self.image_file.delete(save=False) # save=False는 모델의 save 메서드를 다시 호출하지 않도록 합니다.
        super().delete(*args, **kwargs)

    def __str__(self):
        # 객체를 문자열로 표현할 때 이미지 URL을 반환합니다.
        return self.url if self.url else "No Image"


# 사용자 생성 및 슈퍼유저 생성
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해주세요.")
        # 이메일을 소문자로 정규화합니다.
        email = self.normalize_email(email)
        # CustomUser 인스턴스를 생성합니다.
        user = self.model(email=email, **extra_fields)
        # 비밀번호를 해시하여 설정합니다.
        user.set_password(password)
        # 데이터베이스에 사용자를 저장합니다.
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # 슈퍼유저 필드의 기본값을 설정합니다.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")  # 관리자 역할 설정

        # create_user 메서드를 사용하여 슈퍼유저를 생성합니다.
        return self.create_user(email, password, **extra_fields)


# CustomUser 모델 정의
class CustomUser(AbstractUser):
    # Django의 기본 username 필드를 제거하고 email을 사용자 이름으로 사용합니다.
    username = None  # AbstractUser의 username 필드를 제거합니다.

    # 이메일 주소 (필수, 고유)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name="이메일 주소",
    )

    # 비밀번호 (AbstractUser에 이미 포함), password = models.CharField(max_length=128)

    # 닉네임 (필수, 고유)
    nickname = models.CharField(
        max_length=20, unique=True, null=False, blank=False, verbose_name="닉네임"
    )

    # 프로필 이미지 ID (Image 모델의 ForeignKey)
    profile_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,  # 이미지가 삭제되어도 사용자 정보는 유지
        null=True,  # 프로필 이미지가 없을 수도 있습니다.
        blank=True,
        related_name="user_profiles",  # 역참조 이름 설정
    )
    # 사용자 역할 (ENUM = NORMAL, IDOL, MANAGER, ADMIN)
    ROLE_CHOICES = (
        ("NORMAL", "일반 사용자"),
        ("IDOL", "아이돌"),
        ("MANAGER", "매니저"),
        ("ADMIN", "관리자"),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="NORMAL", null=False, blank=False
    )

    # is_superuser와 is_staff는 AbstractUser에 정의
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    # 생성 일시 (자동 기록)
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정 일시 (자동 업데이트)
    updated_at = models.DateTimeField(auto_now=True)

    # 이메일을 사용자 이름 필드로 설정합니다.
    USERNAME_FIELD = "email"
    # 필수 필드를 정의합니다. (password는 기본적으로 포함)
    REQUIRED_FIELDS = ["nickname"]

    # CustomUserManager를 이 모델의 관리자로 설정합니다.
    objects = CustomUserManager()

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "users"
        # Django 관리자 페이지에 표시될 이름을 설정합니다.
        verbose_name = "사용자"
        verbose_name_plural = "사용자들"

    def __str__(self):
        # 객체를 문자열로 표현할 때 이메일 주소를 반환합니다.
        return self.email


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
    # 북마크된 아이돌 (idols 테이블의 ForeignKey - 추후 연결)
    idol_id = models.BigIntegerField(
        null=False, blank=False
    )  # 임시: Idol 모델 ForeignKey로 변경 필요

    # 북마크 생성 일시를 자동으로 기록합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "idols_bookmarks"
        # Django 관리자 페이지에 표시될 이름을 설정합니다.
        verbose_name = "아이돌 즐겨찾기"
        verbose_name_plural = "아이돌 즐겨찾기들"
        # user와 idol_id 조합이 고유해야 합니다. (한 사용자가 같은 아이돌을 두 번 북마크할 수 없음)
        unique_together = ("user", "idol_id")

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용자 이메일과 아이돌 ID를 반환합니다.
        return f"{self.user.email} - 아이돌: {self.idol_id}"


# GroupBookmark 모델 정의
# 다이어그램의 groups_bookmarks 테이블에 해당합니다.
class GroupBookmark(models.Model):
    # 북마크한 사용자 (CustomUser 모델의 ForeignKey)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,  # 사용자가 삭제되면 북마크도 삭제
        null=False,
        blank=False,
        related_name="group_bookmarks",  # 역참조 이름 설정
    )
    # 북마크된 그룹 (groups 테이블의 ForeignKey - 추후 연결)
    group_id = models.BigIntegerField(
        null=False, blank=False
    )  # 임시: Group 모델 ForeignKey로 변경 필요

    # 북마크 생성 일시를 자동으로 기록합니다.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름을 명시적으로 지정합니다.
        db_table = "groups_bookmarks"
        # Django 관리자 페이지에 표시될 이름을 설정합니다.
        verbose_name = "그룹 즐겨찾기"
        verbose_name_plural = "그룹 즐겨찾기들"
        # user와 group_id 조합이 고유해야 합니다. (한 사용자가 같은 그룹을 두 번 북마크할 수 없음)
        unique_together = ("user", "group_id")

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용자 이메일과 그룹 ID를 반환합니다.
        return f"{self.user.email} - 그룹: {self.group_id}"


# 사용자가 자신의 스케줄에 추가한 일정을 기록합니다.
# class UserSchedule(models.Model):
#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         related_name='my_schedules'
#     )
#     # 아이돌 스케줄 또는 그룹 스케줄 중 하나를 참조
#     idol_schedule = models.ForeignKey(
#         IdolSchedule,
#         on_delete=models.CASCADE,
#         null=True, # 둘 중 하나는 null이 될 수 있음
#         blank=True,
#         related_name='user_added_schedules'
#     )
#     group_schedule = models.ForeignKey(
#         GroupSchedule,
#         on_delete=models.CASCADE,
#         null=True, # 둘 중 하나는 null이 될 수 있음
#         blank=True,
#         related_name='user_added_schedules'
#     )
#     added_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'user_schedules'
#         verbose_name = '사용자 스케줄'
#         verbose_name_plural = '사용자 스케줄들'
#         # 한 사용자가 동일한 아이돌 스케줄 또는 그룹 스케줄을 두 번 추가할 수 없도록
#         unique_together = (('user', 'idol_schedule'), ('user', 'group_schedule'))
#
#
#     def __str__(self):
#         if self.idol_schedule:
#             return f"{self.user.email} - 아이돌 스케줄: {self.idol_schedule.description}"
#         elif self.group_schedule:
#             return f"{self.user.email} - 그룹 스케줄: {self.group_schedule.description}"
#         return f"{self.user.email} - 스케줄 없음"