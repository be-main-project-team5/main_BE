from datetime import date

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.idols.models import IdolManager
from apps.users.permissions import IsManagerOrAdmin

from .models import GroupSchedule, IdolSchedule, UserSchedule
from .serializers import (
    GroupScheduleSerializer,
    IdolScheduleSerializer,
    MyScheduleListSerializer,
    UserScheduleCreateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 목록 조회"
    ),
    retrieve=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 상세 조회"
    ),
    create=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 생성"
    ),
    update=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 수정"
    ),
    partial_update=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 부분 수정"
    ),
    destroy=extend_schema(
        tags=["아이돌 스케줄 (Idol Schedules)"], summary="아이돌 스케줄 삭제"
    ),
)
class IdolScheduleViewSet(viewsets.ModelViewSet):
    queryset = IdolSchedule.objects.all()
    serializer_class = IdolScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return IdolSchedule.objects.all()
        elif self.request.user.role == "MANAGER":
            managed_idols = IdolManager.objects.filter(
                user=self.request.user
            ).values_list("idol__id", flat=True)
            return IdolSchedule.objects.filter(idol__id__in=managed_idols)
        elif self.request.user.role == "IDOL":
            return IdolSchedule.objects.filter(idol__user=self.request.user)
        return IdolSchedule.objects.none()

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    def perform_update(self, serializer):
        serializer.save(manager=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 목록 조회"
    ),
    retrieve=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 상세 조회"
    ),
    create=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 생성"
    ),
    update=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 수정"
    ),
    partial_update=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 부분 수정"
    ),
    destroy=extend_schema(
        tags=["그룹 스케줄 (Group Schedules)"], summary="그룹 스케줄 삭제"
    ),
)
class GroupScheduleViewSet(viewsets.ModelViewSet):
    queryset = GroupSchedule.objects.all()
    serializer_class = GroupScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return GroupSchedule.objects.all()
        elif self.request.user.role == "MANAGER":
            managed_group_ids = self.request.user.managed_groups.values_list(
                "id", flat=True
            )
            return GroupSchedule.objects.filter(group__id__in=managed_group_ids)
        return GroupSchedule.objects.none()

    def perform_create(self, serializer):
        group = serializer.validated_data.get("group")
        if not self.request.user.is_staff and group.manager != self.request.user:
            raise PermissionDenied("이 그룹의 스케줄을 생성할 권한이 없습니다.")
        serializer.save(author=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=["내 스케줄 (My Schedules)"], summary="내 스케줄 목록 조회"
    ),
    retrieve=extend_schema(
        tags=["내 스케줄 (My Schedules)"], summary="내 스케줄 상세 조회"
    ),
    create=extend_schema(
        tags=["내 스케줄 (My Schedules)"], summary="내 스케줄에 추가 (북마크)"
    ),
    destroy=extend_schema(
        tags=["내 스케줄 (My Schedules)"], summary="내 스케줄에서 삭제 (북마크)"
    ),
)
class UserScheduleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSchedule.objects.filter(user=self.request.user).select_related(
            "idol_schedule", "group_schedule"
        )

    def get_serializer_class(self):
        if self.action == "create":
            return UserScheduleCreateSerializer
        return MyScheduleListSerializer


@extend_schema_view(
    list=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 목록 조회"
    ),
    retrieve=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 상세 조회"
    ),
    create=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 생성"
    ),
    update=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 수정"
    ),
    partial_update=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 부분 수정"
    ),
    destroy=extend_schema(
        tags=["매니저 스케줄 관리 (Manager)"], summary="담당 아이돌 스케줄 삭제"
    ),
)
class ManagerScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = IdolScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "MANAGER":
            managed_idols = IdolManager.objects.filter(
                user=self.request.user
            ).values_list("idol", flat=True)
            return IdolSchedule.objects.filter(idol__in=managed_idols)
        return IdolSchedule.objects.none()

    def perform_create(self, serializer):
        idol_id = self.request.data.get("idol")
        if not idol_id:
            raise ValidationError({"idol": "This field is required."})

        managed_idols = IdolManager.objects.filter(user=self.request.user).values_list(
            "idol__id", flat=True
        )
        if int(idol_id) not in managed_idols:
            raise PermissionDenied("이 아이돌의 스케줄을 생성할 권한이 없습니다.")
        serializer.save(manager=self.request.user)

    def perform_update(self, serializer):
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()


@extend_schema(
    tags=["매니저 메인보드 (Manager Mainboard)"],
    summary="매니저 메인보드 오늘 스케줄 조회",
    description="로그인한 매니저가 담당하는 아이돌들의 오늘자 스케줄을 조회합니다.",
)
class ManagerMainboardView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def get(self, request):
        user = request.user
        if user.role != "MANAGER":
            return Response(
                {"detail": "매니저만 접근할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        managed_idols = IdolManager.objects.filter(user=user).values_list(
            "idol__id", flat=True
        )
        today = date.today()
        schedules = IdolSchedule.objects.filter(
            idol__id__in=managed_idols, start_time__date=today
        ).order_by("start_time")

        serializer = IdolScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
