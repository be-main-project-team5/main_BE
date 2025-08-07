from rest_framework import serializers

from .models import Idol, IdolSchedule


class IdolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idol
        fields = "__all__"


class IdolScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdolSchedule
        # fields에 id, title, start_time, end_time, description, is_public, idol, manager를 명시합니다.
        fields = [
            "id",
            "title",
            "start_time",
            "end_time",
            "description",
            "is_public",
            "idol",
        ]
        read_only_fields = ["id", "idol"]
