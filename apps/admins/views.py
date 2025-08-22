from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
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


@extend_schema(
    tags=["관리자 (Admin)"],
    summary="전체 사용자 목록 조회",
    description="모든 사용자의 목록을 조회합니다. 역할(role) 필터링, 이메일/닉네임 검색, 정렬 기능이 있습니다.",
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
    ordering = ["-date_joined"]


@extend_schema(
    tags=["관리자 (Admin)"],
    summary="매니저 계정 생성",
    description="새로운 매니저 계정을 생성합니다. 관리자만 가능합니다.",
)
class ManagerCreateView(CreateAPIView):
    """매니저 계정을 생성하는 API 뷰"""

    serializer_class = ManagerCreateSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    tags=["관리자 (Admin)"],
    summary="아이돌 계정 생성",
    description="새로운 아이돌 계정을 생성합니다. 관리자만 가능합니다.",
)
class IdolCreateView(CreateAPIView):
    """아이돌 계정을 생성하는 API 뷰"""

    serializer_class = IdolCreateSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    tags=["관리자 (Admin)"],
    summary="사용자 계정 삭제",
    description="특정 사용자 계정을 삭제합니다. 관리자만 가능합니다.",
)
class UserDeleteView(DestroyAPIView):
    """사용자 계정을 삭제하는 API 뷰"""

    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]


@extend_schema_view(
    list=extend_schema(tags=["관리자 (Admin)"], summary="매니저-아이돌 관계 목록 조회"),
    retrieve=extend_schema(
        tags=["관리자 (Admin)"], summary="매니저-아이돌 관계 상세 조회"
    ),
    create=extend_schema(tags=["관리자 (Admin)"], summary="매니저-아이돌 관계 생성"),
    destroy=extend_schema(tags=["관리자 (Admin)"], summary="매니저-아이돌 관계 삭제"),
)
class IdolManagerViewSet(viewsets.ModelViewSet):
    """매니저-아이돌 관계 관리 API 뷰"""

    queryset = IdolManager.objects.all()
    serializer_class = IdolManagerCreateSerializer
    permission_classes = [IsAdminUser]
    http_method_names = [
        "get",
        "post",
        "delete",
        "head",
        "options",
    ]  # update, partial_update 제외
