from datetime import timedelta

from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schedules.models import GroupSchedule, IdolSchedule

from .models import Alarm
from .serializers import AlarmSerializer


class AlarmListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        alarms = Alarm.objects.filter(user=request.user).order_by("-created_at")
        serializer = AlarmSerializer(alarms, many=True)
        return Response(serializer.data)


class AlarmCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        사용자 요청: idol_schedule_id 또는 group_schedule_id를 전달
        → 해당 스케줄의 시작 시간 기준으로 scheduled_time 설정
        → 알람 생성
        """
        user = request.user
        idol_schedule_id = request.data.get("idol_schedule_id")
        group_schedule_id = request.data.get("group_schedule_id")

        if idol_schedule_id:
            schedule = get_object_or_404(IdolSchedule, id=idol_schedule_id)
            message = (
                f"[{schedule.idol.name}] '{schedule.title}' 스케줄 시작 10분 전 알림"
            )
            scheduled_time = schedule.start_time - timedelta(minutes=10)
            alarm = Alarm.objects.create(
                user=user,
                idol_schedule=schedule,
                message=message,
                scheduled_time=scheduled_time,
            )
        elif group_schedule_id:
            schedule = get_object_or_404(GroupSchedule, id=group_schedule_id)
            message = (
                f"[{schedule.group.name}] '{schedule.title}' 스케줄 시작 10분 전 알림"
            )
            scheduled_time = schedule.start_time - timedelta(minutes=10)
            alarm = Alarm.objects.create(
                user=user,
                group_schedule=schedule,
                message=message,
                scheduled_time=scheduled_time,
            )
        else:
            return Response(
                {
                    "detail": "idol_schedule_id 또는 group_schedule_id 중 하나는 필요합니다."
                },
                status=400,
            )

        serializer = AlarmSerializer(alarm)
        return Response(serializer.data, status=201)


class AlarmDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        alarm = get_object_or_404(Alarm, id=id, user=request.user)
        serializer = AlarmSerializer(alarm)
        return Response(serializer.data)

    def patch(self, request, id):
        alarm = get_object_or_404(Alarm, id=id, user=request.user)
        alarm.is_read = True
        alarm.save()
        return Response({"detail": "알람 읽음 처리 완료"})

    def delete(self, request, id):
        alarm = get_object_or_404(Alarm, id=id, user=request.user)
        alarm.delete()
        return Response({"detail": "알람 삭제 완료"}, status=204)
