from rest_framework import serializers

from .models import GroupBookmark, IdolBookmark


class IdolBookmarkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    idol_name = serializers.ReadOnlyField(source="idol.name")

    class Meta:
        model = IdolBookmark
        fields = ["id", "user", "idol", "idol_name", "created_at"]
        read_only_fields = ["id", "user", "idol_name", "created_at"]


class GroupBookmarkSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    group_name = serializers.ReadOnlyField(source="group.name")

    class Meta:
        model = GroupBookmark
        fields = ["id", "user", "group", "group_name", "created_at"]
        read_only_fields = ["id", "user", "group_name", "created_at"]
