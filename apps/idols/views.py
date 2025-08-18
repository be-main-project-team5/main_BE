from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Idol, IdolManager
from .serializers import IdolSerializer, IdolGroupSerializer
from apps.common.permissions import IsManagerOrAdminOrReadOnly


class IdolListView(generics.ListAPIView):
    queryset = Idol.objects.all()
    serializer_class = IdolSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인 된 사용자 이용 가능
    filter_backends = [SearchFilter]
    search_fields = ['name']

    # 특정 아이돌 상세 조회


class IdolDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 로그인 된 사용자 이용 가능

    def get(self, request, id):
        idol = get_object_or_404(Idol, id=id)
        serializer = IdolSerializer(idol)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 아이돌 스케줄 조회 및 생성
class IdolScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        idol = get_object_or_404(Idol, id=id)
        schedules = idol.schedules.all().order_by("start_time")
        serializer = IdolScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        idol = get_object_or_404(Idol, id=id)
        is_manager = IdolManager.objects.filter(user=request.user, idol=idol).exists()
        if not is_manager:
            return Response(
                {"detail": "이 아이돌의 스케줄 등록 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["idol"] = idol.id

        serializer = IdolScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IdolScheduleDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, idol_id, schedule_id):
        schedule = get_object_or_404(IdolSchedule, id=schedule_id, idol_id=idol_id)
        serializer = IdolScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, idol_id, schedule_id):
        idol = get_object_or_404(Idol, id=idol_id)
        schedule = get_object_or_404(IdolSchedule, id=schedule_id, idol=idol)

        is_manager = IdolManager.objects.filter(user=request.user, idol=idol).exists()
        if not is_manager:
            return Response(
                {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = IdolScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, idol_id, schedule_id):
        idol = get_object_or_404(Idol, id=idol_id)
        schedule = get_object_or_404(IdolSchedule, id=schedule_id, idol=idol)

        is_manager = IdolManager.objects.filter(user=request.user, idol=idol).exists()
        if not is_manager:
            return Response(
                {"detail": "이 아이돌의 스케줄 삭제 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        schedule.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


from apps.schedules.models import IdolSchedule
from apps.schedules.serializers import IdolScheduleSerializer
from datetime import date


class IdolGroupUpdateView(generics.UpdateAPIView):
    """아이돌의 그룹을 변경하는 API 뷰"""
    queryset = Idol.objects.all()
    serializer_class = IdolGroupSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        # 매니저는 자신이 담당하는 아이돌만 수정 가능
        if self.request.user.role == 'MANAGER':
            managed_idol_ids = IdolManager.objects.filter(user=self.request.user).values_list('idol_id', flat=True)
            return Idol.objects.filter(id__in=managed_idol_ids)
        # 관리자는 모든 아이돌 수정 가능
        return Idol.objects.all()

class IdolMainboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'IDOL':
            return Response(
                {"detail": "아이돌만 접근할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            idol = Idol.objects.get(user=user)
        except Idol.DoesNotExist:
            return Response(
                {"detail": "해당 사용자와 연결된 아이돌 정보가 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        today = date.today()
        schedules = IdolSchedule.objects.filter(
            idol=idol,
            start_time__date=today
        ).order_by('start_time')

        serializer = IdolScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
