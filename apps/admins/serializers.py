from rest_framework import serializers

from apps.idols.models import Idol, IdolManager
from apps.users.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    """회원 목록을 위한 시리얼라이저"""

    class Meta:
        model = CustomUser
        fields = ["id", "email", "nickname", "role", "is_staff", "date_joined"]


class BaseUserCreateSerializer(serializers.ModelSerializer):
    """사용자 생성을 위한 기본 시리얼라이저 (비밀번호 처리 포함)"""

    class Meta:
        model = CustomUser
        fields = ["email", "password", "nickname"]  # username 필드 제거
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # create_user 메서드 호출 방식을 모델 매니저에 맞게 수정
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data.get("nickname", ""),
        )
        return user


class ManagerCreateSerializer(BaseUserCreateSerializer):
    """매니저 계정 생성을 위한 시리얼라이저"""

    def create(self, validated_data):
        # create_user를 오버라이드하는 대신, validated_data에 역할 정보를 추가합니다.
        validated_data["role"] = "MANAGER"
        validated_data["is_staff"] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user


class IdolCreateSerializer(BaseUserCreateSerializer):
    """아이돌 계정 생성을 위한 시리얼라이저"""

    def create(self, validated_data):
        user = super().create(validated_data)
        user.role = "IDOL"
        user.save()
        # 아이돌 객체 생성 추가
        Idol.objects.create(user=user, name=validated_data.get("nickname"))
        return user


class IdolManagerCreateSerializer(serializers.ModelSerializer):
    """매니저-아이돌 관계 생성을 위한 시리얼라이저"""

    class Meta:
        model = IdolManager
        fields = ["user", "idol"]  # user는 매니저, idol은 아이돌
