from rest_framework import serializers

from apps.common.mixins import ImageUpdateSerializerMixin
from apps.users.models import CustomUser, Image  # CustomUser 임포트 추가

from .models import Group


class GroupMemberSerializer(serializers.ModelSerializer):
    """
    그룹 구성원(매니저, 아이돌)의 사용자 정보를 위한 Serializer
    """

    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "nickname", "role", "profile_image_url"]

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None


# Image 모델을 위한 Serializer (users 앱에서 가져옴)
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "file_size", "created_at"]
        read_only_fields = ["id", "url", "file_size", "created_at"]


# Group 모델의 데이터를 JSON 형태로 변환하거나, JSON 데이터를 Group 모델 인스턴스로 변환하는 역할을 합니다.
# 이 시리얼라이저는 Django REST Framework의 ModelSerializer를 상속받아, 모델 필드에 대한 자동 매핑 기능을 활용합니다.
# 'apps/groups/views.py'의 GroupViewSet에서 Group 모델의 데이터를 직렬화하고 역직렬화하는 데 사용됩니다.
class GroupSerializer(ImageUpdateSerializerMixin, serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())
    logo_image = serializers.ImageField(
        required=False, allow_null=True, write_only=True
    )
    logo_image_url = serializers.SerializerMethodField()  # 읽기 전용 필드 추가

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "debut_date",
            "agency",
            "manager",
            "logo_image",
            "logo_image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_logo_image_url(self, obj):
        if obj.logo_image:
            return obj.logo_image.url
        return None

    def create(self, validated_data):
        logo_image_file = validated_data.pop("logo_image", None)

        group = Group.objects.create(**validated_data)

        if logo_image_file:
            image_instance = Image.objects.create(image_file=logo_image_file)
            group.logo_image = image_instance
            group.save()
        return group

    def update(self, instance, validated_data):
        # Use the mixin to handle the logo image update
        self._update_image(instance, validated_data, "logo_image")

        # Update other fields
        instance.name = validated_data.get("name", instance.name)
        instance.debut_date = validated_data.get("debut_date", instance.debut_date)
        instance.agency = validated_data.get("agency", instance.agency)

        instance.save()
        return instance