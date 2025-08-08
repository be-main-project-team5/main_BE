from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.storage import default_storage
from rest_framework import serializers

from .models import CustomUser, Image

# from apps.idols.serializers import IdolScheduleSerializer
# from apps.groups.serializers import GroupScheduleSerializer


# Image 모델을 위한 Serializer
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "file_size", "created_at"]
        read_only_fields = ["id", "url", "file_size", "created_at"]


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )
    profile_image = serializers.ImageField(
        required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ["email", "nickname", "password", "password_confirm", "profile_image"]
        extra_kwargs = {
            "email": {"required": True},
            "nickname": {"required": True, "min_length": 2, "max_length": 20},
        }

    def validate(self, data):
        # 비밀번호와 비밀번호 확인 일치 여부 검사
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "비밀번호가 일치하지 않습니다."}
            )
        # 이메일 중복 검사
        if CustomUser.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "이미 사용 중인 이메일 주소입니다."}
            )
        # 닉네임 중복 검사
        if CustomUser.objects.filter(nickname=data["nickname"]).exists():
            raise serializers.ValidationError(
                {"nickname": "이미 사용 중인 닉네임입니다."}
            )

        return data

    def create(self, validated_data):
        profile_image_file = validated_data.pop("profile_image", None)

        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
        )

        if profile_image_file:
            image_instance = Image.objects.create(image_file=profile_image_file)
            user.profile_image = image_instance
            user.save()
        return user


# 로그인
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            # Django의 authenticate 함수를 사용하여 사용자 인증
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "이메일 또는 비밀번호가 일치하지 않습니다.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                "이메일과 비밀번호를 모두 입력해주세요.", code="authorization"
            )

        data["user"] = user
        return data


# 사용자 프로필 조회 및 수정
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        required=False, allow_null=True, write_only=True
    )
    profile_image_url = serializers.SerializerMethodField()  # 읽기 전용 필드 추가

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "nickname",
            "profile_image",
            "profile_image_url",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "created_at",
            "updated_at",
        ]  # 이메일, 역할, 생성/수정일은 읽기 전용
        extra_kwargs = {
            "nickname": {"required": False, "min_length": 2, "max_length": 20},
        }

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

    def validate_nickname(self, value):
        # 닉네임 중복 검사 (수정 시 본인 닉네임은 허용)
        if (
            self.instance
            and CustomUser.objects.exclude(id=self.instance.id)
            .filter(nickname=value)
            .exists()
        ):
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def update(self, instance, validated_data):
        profile_image_file = validated_data.pop("profile_image", None)

        # 닉네임 업데이트
        instance.nickname = validated_data.get("nickname", instance.nickname)

        # 프로필 이미지 처리
        if profile_image_file is not None:  # 이미지가 제공된 경우 (새 이미지 또는 null)
            # 기존 이미지 삭제
            if instance.profile_image:
                # 파일 시스템에서 이미지 파일 삭제
                if default_storage.exists(
                    instance.profile_image.url.replace(settings.MEDIA_URL, "")
                ):
                    default_storage.delete(
                        instance.profile_image.url.replace(settings.MEDIA_URL, "")
                    )
                instance.profile_image.delete()  # Image 모델 인스턴스 삭제

            if profile_image_file:  # 새 이미지가 있는 경우
                new_image = Image(image_file=profile_image_file)
                new_image.save()
                instance.profile_image = new_image
            else:  # 이미지를 null로 설정 (삭제 요청)
                instance.profile_image = None
        elif (
            "profile_image" in self.context["request"].data
            and self.context["request"].data["profile_image"] == "null"
        ):
            # 클라이언트에서 명시적으로 "profile_image": null을 보낸 경우 (이미지 삭제)
            if instance.profile_image:
                if default_storage.exists(
                    instance.profile_image.url.replace(settings.MEDIA_URL, "")
                ):
                    default_storage.delete(
                        instance.profile_image.url.replace(settings.MEDIA_URL, "")
                    )
                instance.profile_image.delete()
            instance.profile_image = None

        instance.save()
        return instance


# 비밀번호 변경
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_new_password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )

    def validate(self, data):
        user = self.context["request"].user
        # 현재 비밀번호 확인
        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "현재 비밀번호가 일치하지 않습니다."}
            )

        # 새 비밀번호와 확인 비밀번호 일치 여부 검사
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "새 비밀번호가 일치하지 않습니다."}
            )

        # 새 비밀번호 유효성 검사
        try:
            validate_password(data["new_password"], user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data


# 회원 탈퇴
class UserDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context["request"].user
        # 비밀번호 확인
        if not user.check_password(data["password"]):
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return data



