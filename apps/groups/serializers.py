from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import serializers

from apps.users.models import Image  # Image 모델 임포트

from .models import Group, GroupSchedule


# Image 모델을 위한 Serializer (users 앱에서 가져옴)
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "file_size", "created_at"]
        read_only_fields = ["id", "url", "file_size", "created_at"]


# Group 모델의 데이터를 JSON 형태로 변환하거나, JSON 데이터를 Group 모델 인스턴스로 변환하는 역할을 합니다.
# 이 시리얼라이저는 Django REST Framework의 ModelSerializer를 상속받아, 모델 필드에 대한 자동 매핑 기능을 활용합니다.
# 'apps/groups/views.py'의 GroupViewSet에서 Group 모델의 데이터를 직렬화하고 역직렬화하는 데 사용됩니다.
class GroupSerializer(serializers.ModelSerializer):
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
        logo_image_file = validated_data.pop("logo_image", None)

        # 기본 필드 업데이트
        instance.name = validated_data.get("name", instance.name)
        instance.debut_date = validated_data.get("debut_date", instance.debut_date)
        instance.agency = validated_data.get("agency", instance.agency)

        # 로고 이미지 처리
        if logo_image_file is not None:  # 이미지가 제공된 경우 (새 이미지 또는 null)
            # 기존 이미지 삭제
            if instance.logo_image:
                # 파일 시스템에서 이미지 파일 삭제
                if default_storage.exists(
                    instance.logo_image.url.replace(settings.MEDIA_URL, "")
                ):
                    default_storage.delete(
                        instance.logo_image.url.replace(settings.MEDIA_URL, "")
                    )
                instance.logo_image.delete()  # Image 모델 인스턴스 삭제

            if logo_image_file:  # 새 이미지가 있는 경우
                new_image = Image(image_file=logo_image_file)
                new_image.save()
                instance.logo_image = new_image
            else:  # 이미지를 null로 설정 (삭제 요청)
                instance.logo_image = None
        elif (
            "logo_image" in self.context["request"].data
            and self.context["request"].data["logo_image"] == "null"
        ):
            # 클라이언트에서 명시적으로 "logo_image": null을 보낸 경우 (이미지 삭제)
            if instance.logo_image:
                if default_storage.exists(
                    instance.logo_image.url.replace(settings.MEDIA_URL, "")
                ):
                    default_storage.delete(
                        instance.logo_image.url.replace(settings.MEDIA_URL, "")
                    )
                instance.logo_image.delete()
            instance.logo_image = None

        instance.save()
        return instance


class GroupScheduleSerializer(serializers.ModelSerializer):
    """
    GroupSchedule 모델을 위한 시리얼라이저
    """

    class Meta:
        model = GroupSchedule
        fields = [
            "id",
            "group",
            "start_time",
            "end_time",
            "location",
            "description",
            "is_public",
            "created_at",
            "updated_at",
        ]
        # group 필드는 URL에서 자동으로 주입되므로, 생성/수정 시에는 읽기 전용으로 처리합니다.
        read_only_fields = ("group",)
