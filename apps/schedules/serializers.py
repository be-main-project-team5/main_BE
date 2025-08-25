from rest_framework import serializers

from .models import GroupSchedule, IdolSchedule, UserSchedule


class IdolScheduleSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )  # 현재 로그인한 사용자를 manager로 자동 설정

    class Meta:
        model = IdolSchedule
        fields = "__all__"
        # read_only_fields = ('manager',) # HiddenField를 사용하므로 필요 없음

    def create(self, validated_data):
        # manager 필드는 HiddenField에서 자동으로 설정되므로, validated_data에 이미 포함되어 있음
        return super().create(validated_data)


class GroupScheduleSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GroupSchedule
        fields = "__all__"


class UserScheduleCreateSerializer(serializers.ModelSerializer):
    idol_schedule = serializers.PrimaryKeyRelatedField(
        queryset=IdolSchedule.objects.all(), required=False, allow_null=True
    )
    group_schedule = serializers.PrimaryKeyRelatedField(
        queryset=GroupSchedule.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = UserSchedule
        fields = ["id", "idol_schedule", "group_schedule"]
        read_only_fields = ["id"]

    def validate(self, data):
        if not data.get("idol_schedule") and not data.get("group_schedule"):
            raise serializers.ValidationError(
                "A schedule (idol or group) must be provided."
            )
        if data.get("idol_schedule") and data.get("group_schedule"):
            raise serializers.ValidationError(
                "Cannot provide both an idol and group schedule."
            )

        user = self.context["request"].user
        schedule_field = (
            "idol_schedule" if data.get("idol_schedule") else "group_schedule"
        )
        schedule = data.get(schedule_field)

        if UserSchedule.objects.filter(
            user=user, **{schedule_field: schedule}
        ).exists():
            raise serializers.ValidationError(
                {"detail": "This schedule is already in your list."}, code="unique"
            )
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class MyScheduleListSerializer(serializers.ModelSerializer):
    schedule_type = serializers.SerializerMethodField()
    schedule_details = serializers.SerializerMethodField()

    class Meta:
        model = UserSchedule
        fields = ["id", "schedule_type", "schedule_details"]

    def get_schedule_type(self, obj):
        if obj.idol_schedule:
            return "idol"
        if obj.group_schedule:
            return "group"
        return None

    def get_schedule_details(self, obj):
        if obj.idol_schedule:
            return IdolScheduleSerializer(obj.idol_schedule).data
        if obj.group_schedule:
            return GroupScheduleSerializer(obj.group_schedule).data
        return None
