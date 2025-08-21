from datetime import date

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsManagerOrAdminOrReadOnly
from apps.schedules.models import IdolSchedule
from apps.schedules.serializers import IdolScheduleSerializer

from .models import Idol, IdolManager
from .serializers import IdolGroupSerializer, IdolSerializer


@extend_schema(
    tags=["아이돌 (Idols)"],
    summary="아이돌 목록 조회",
    description="모든 아이돌의 목록을 조회합니다. `?search=` 쿼리 파라미터로 이름을 검색할 수 있습니다."
)
class IdolListView(generics.ListAPIView):
    queryset = Idol.objects.all()
    serializer_class = IdolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


@extend_schema(
    tags=["아이돌 (Idols)"],
    summary="아이돌 상세 정보 조회",
    description="특정 아이돌의 상세 정보를 조회합니다."
)
class IdolDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        idol = get_object_or_404(Idol, id=id)
        serializer = IdolSerializer(idol)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"],
        summary="특정 아이돌의 전체 스케줄 조회",
        description="특정 아이돌에게 등록된 모든 스케줄을 시간순으로 조회합니다."
    ),
    post=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"],
        summary="특정 아이돌의 스케줄 생성",
        description="특정 아이돌에게 새 스케줄을 등록합니다. 해당 아이돌의 매니저만 가능합니다."
    )
)
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


@extend_schema_view(
    get=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"],
        summary="아이돌 스케줄 상세 조회",
        description="특정 아이돌의 특정 스케줄 하나를 상세 조회합니다."
    ),
    put=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"],
        summary="아이돌 스케줄 수정",
        description="아이돌 스케줄을 수정합니다. 해당 아이돌의 매니저만 가능합니다."
    ),
    delete=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"],
        summary="아이돌 스케줄 삭제",
        description="아이돌 스케줄을 삭제합니다. 해당 아이돌의 매니저만 가능합니다."
    )
)
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


@extend_schema(
    tags=["아이돌 (Idols)"],
    summary="아이돌의 소속 그룹 변경",
    description="특정 아이돌의 소속 그룹 정보를 변경합니다. 매니저 또는 관리자만 가능합니다."
)
class IdolGroupUpdateView(generics.UpdateAPIView):
    """아이돌의 그룹을 변경하는 API 뷰"""

    queryset = Idol.objects.all()
    serializer_class = IdolGroupSerializer
    permission_classes = [IsManagerOrAdminOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        # 매니저는 자신이 담당하는 아이돌만 수정 가능
        if self.request.user.role == "MANAGER":
            managed_idol_ids = IdolManager.objects.filter(
                user=self.request.user
            ).values_list("idol_id", flat=True)
            return Idol.objects.filter(id__in=managed_idol_ids)
        # 관리자는 모든 아이돌 수정 가능
        return Idol.objects.all()


@extend_schema(
    tags=["아이돌 메인보드 (Idol Mainboard)"],
    summary="아이돌 메인보드 오늘 스케줄 조회",
    description="로그인한 아이돌 본인의 오늘자 스케줄을 조회합니다."
)
class IdolMainboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "IDOL":
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
            idol=idol, start_time__date=today
        ).order_by("start_time")

        serializer = IdolScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["매니저 메인보드 (Manager Mainboard)"],
    summary="매니저 메인보드 스케줄 조회",
    description="로그인한 매니저가 담당하는 아이돌들의 오늘자 스케줄과 전체 스케줄을 조회합니다."
)
class ManagerMainboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "MANAGER":
            return Response(
                {"detail": "매니저만 접근할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        managed_idols = Idol.objects.filter(managers__user=user)
        if not managed_idols.exists():
            return Response(
                {"detail": "담당하는 아이돌이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        today = date.today()
        today_schedules = IdolSchedule.objects.filter(
            idol__in=managed_idols, start_time__date=today
        ).order_by("start_time")

        all_schedules = IdolSchedule.objects.filter(idol__in=managed_idols).order_by(
            "start_time"
        )

        today_serializer = IdolScheduleSerializer(today_schedules, many=True)
        all_serializer = IdolScheduleSerializer(all_schedules, many=True)

        return Response(
            {
                "today_schedules": today_serializer.data,
                "all_schedules": all_serializer.data,
            },
            status=status.HTTP_200_OK,
        )