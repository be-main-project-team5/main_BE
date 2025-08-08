from rest_framework import serializers
from .models import IdolSchedule, GroupSchedule, UserSchedule

class IdolScheduleSerializer(serializers.ModelSerializer):
    manager = serializers.HiddenField(default=serializers.CurrentUserDefault()) # 현재 로그인한 사용자를 manager로 자동 설정

    class Meta:
        model = IdolSchedule
        fields = '__all__'
        # read_only_fields = ('manager',) # HiddenField를 사용하므로 필요 없음

    def create(self, validated_data):
        # manager 필드는 HiddenField에서 자동으로 설정되므로, validated_data에 이미 포함되어 있음
        return super().create(validated_data)

class GroupScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupSchedule
        fields = '__all__'
        read_only_fields = ('author',) # author 필드는 자동으로 설정되므로 읽기 전용


class UserScheduleCreateSerializer(serializers.ModelSerializer):
    # 아이돌 스케줄 ID 또는 그룹 스케줄 ID 중 하나만 필수
    idol_schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=IdolSchedule.objects.all(),
        source="idol_schedule",
        required=False,
        allow_null=True,
    )
    group_schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=GroupSchedule.objects.all(), source='group_schedule', required=False, allow_null=True
    )

    class Meta:
        model = UserSchedule
        fields = ["idol_schedule_id", "group_schedule_id"]

    def validate(self, data):
        idol_schedule = data.get("idol_schedule")
        group_schedule = data.get("group_schedule")

        if not idol_schedule and not group_schedule:
            raise serializers.ValidationError(
                "아이돌 스케줄 또는 그룹 스케줄 중 하나는 선택해야 합니다."
            )
        if idol_schedule and group_schedule:
            raise serializers.ValidationError(
                "아이돌 스케줄과 그룹 스케줄을 동시에 추가할 수 없습니다."
            )

        # 이미 추가된 스케줄인지 확인
        user = self.context["request"].user
        if (
            idol_schedule
            and UserSchedule.objects.filter(
                user=user, idol_schedule=idol_schedule
            ).exists()
        ):
            raise serializers.ValidationError(
                "이미 내 스케줄에 추가된 아이돌 일정입니다.", code="duplicate_entry"
            )
        if (
            group_schedule
            and UserSchedule.objects.filter(
                user=user, group_schedule=group_schedule
            ).exists()
        ):
            raise serializers.ValidationError(
                "이미 내 스케줄에 추가된 그룹 일정입니다.", code="duplicate_entry"
            )

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        return UserSchedule.objects.create(user=user, **validated_data)


class MyScheduleListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # UserSchedule의 ID
    schedule_id = serializers.IntegerField(read_only=True)  # 원본 스케줄의 ID
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    location = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    entity_type = serializers.CharField(read_only=True)  # 'idol' 또는 'group'
    entity_name = serializers.CharField(read_only=True)  # 아이돌 이름 또는 그룹 이름
