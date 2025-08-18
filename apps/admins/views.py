from django_filters.rest_framework import DjangoFilterBackend  # 추가
from rest_framework import filters, viewsets
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser

from apps.idols.models import IdolManager
from apps.users.models import CustomUser

from .serializers import (
    IdolCreateSerializer,
    IdolManagerCreateSerializer,
    ManagerCreateSerializer,
    UserListSerializer,
)


class UserListView(ListAPIView):
    """전체 사용자 목록을 반환하는 API 뷰 (검색, 정렬, 필터링 기능 추가)"""

    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["role"]
    search_fields = ["email", "nickname"]
    ordering_fields = ["nickname", "role", "date_joined"]
    ordering = ["-date_joined"]  # 기��� 정렬: 최신 가입 순


class ManagerCreateView(CreateAPIView):
    """매니저 계정을 생성하는 API 뷰"""

    serializer_class = ManagerCreateSerializer
    permission_classes = [IsAdminUser]  # 관리자만 접근 가능


class IdolCreateView(CreateAPIView):
    """아이돌 계정을 생성하는 API 뷰"""

    serializer_class = IdolCreateSerializer
    permission_classes = [IsAdminUser]  # 관리자만 접근 가능


class UserDeleteView(DestroyAPIView):
    """사용자 계정을 삭제하는 API 뷰"""

    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]


class IdolManagerViewSet(viewsets.ModelViewSet):
    """매니저-아이돌 관계 관리 API 뷰"""

    queryset = IdolManager.objects.all()
    serializer_class = IdolManagerCreateSerializer
    permission_classes = [IsAdminUser]
