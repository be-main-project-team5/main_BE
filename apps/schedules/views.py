from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from .models import IdolSchedule, GroupSchedule
from .serializers import IdolScheduleSerializer, GroupScheduleSerializer
from apps.users.permissions import IsManagerOrAdmin
from apps.idols.models import IdolManager # IdolManager 모델 임포트

class IdolScheduleViewSet(viewsets.ModelViewSet):
    queryset = IdolSchedule.objects.all()
    serializer_class = IdolScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        # 관리자는 모든 스케줄 조회 가능
        if self.request.user.role == 'ADMIN':
            return IdolSchedule.objects.all()
        # 매니저는 자신이 담당하는 아이돌의 스케줄만 조회 가능
        elif self.request.user.role == 'MANAGER':
            managed_idols = IdolManager.objects.filter(user=self.request.user).values_list('idol__id', flat=True)
            return IdolSchedule.objects.filter(idol__id__in=managed_idols)
        # 그 외 사용자 (아이돌 포함)는 자신의 아이돌 스케줄만 조회 가능
        elif self.request.user.role == 'IDOL':
            return IdolSchedule.objects.filter(idol__user=self.request.user)
        return IdolSchedule.objects.none() # 권한 없는 경우 빈 쿼리셋 반환

    def perform_create(self, serializer):
        # 스케줄 생성 시 현재 로그인한 사용자를 manager로 설정
        serializer.save(manager=self.request.user)

    def perform_update(self, serializer):
        # 스케줄 수정 시 현재 로그인한 사용자를 manager로 설정 (선택 사항, 필요에 따라)
        serializer.save(manager=self.request.user)

class GroupScheduleViewSet(viewsets.ModelViewSet):
    queryset = GroupSchedule.objects.all()
    serializer_class = GroupScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def perform_create(self, serializer):
        # 스케줄 생성 시 현재 로그인한 사용자를 author로 설정
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # 스케줄 수정 시 현재 로그인한 사용자를 author로 설정 (선택 사항, 필요에 따라)
        serializer.save(author=self.request.user)


from rest_framework.permissions import IsAuthenticated
from .models import UserSchedule
from .serializers import MyScheduleListSerializer

class UserScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserSchedule.objects.all()
    serializer_class = MyScheduleListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자의 UserSchedule만 반환
        return UserSchedule.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        # 특정 UserSchedule 조회 시, 해당 스케줄의 상세 정보를 포함하여 반환
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # IdolSchedule 또는 GroupSchedule의 상세 정보 추가
        if instance.idol_schedule:
            data['schedule_details'] = IdolScheduleSerializer(instance.idol_schedule).data
        elif instance.group_schedule:
            data['schedule_details'] = GroupScheduleSerializer(instance.group_schedule).data
        return Response(data)


class ManagerScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = IdolScheduleSerializer
    permission_classes = [IsManagerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "MANAGER":
            # 현재 매니저가 담당하는 아이돌 목록을 가져옵니다.
            managed_idols = IdolManager.objects.filter(user=self.request.user).values_list('idol', flat=True)
            # 담당 아이돌의 스케줄만 필터링합니다.
            return IdolSchedule.objects.filter(idol__in=managed_idols)
        return IdolSchedule.objects.none()

    def perform_create(self, serializer):
        # 스케줄 생성 시, 요청한 사용자가 담당하는 아이돌인지 확인
        idol_id = self.request.data.get('idol')
        if not idol_id:
            raise ValidationError({"idol": "This field is required."})
        
        managed_idols = IdolManager.objects.filter(user=self.request.user).values_list('idol__id', flat=True)
        if int(idol_id) not in managed_idols:
            raise PermissionDenied("이 아이돌의 스케줄을 생성할 권한이 없습니다.")
        serializer.save(manager=self.request.user)

    def perform_update(self, serializer):
        # 스케줄 업데이트 시, 해당 스케줄이 매니저가 담당하는 아이돌의 것인지 확인
        self.check_object_permissions(self.request, serializer.instance)
        serializer.save()

    def perform_destroy(self, instance):
        # 스케줄 삭제 시, 해당 스케줄이 매니저가 담당하는 아이돌의 것인지 확인
        self.check_object_permissions(self.request, instance)
        instance.delete()


from rest_framework.views import APIView
from datetime import date


class ManagerMainboardView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def get(self, request):
        user = request.user
        if user.role != 'MANAGER':
            return Response(
                {"detail": "매니저만 접근할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        managed_idols = IdolManager.objects.filter(user=user).values_list('idol__id', flat=True)
        today = date.today()
        schedules = IdolSchedule.objects.filter(
            idol__id__in=managed_idols,
            start_time__date=today
        ).order_by('start_time')

        serializer = IdolScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)