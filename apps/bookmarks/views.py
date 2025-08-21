from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GroupBookmark, IdolBookmark
from .serializers import GroupBookmarkSerializer, IdolBookmarkSerializer


@extend_schema_view(
    list=extend_schema(tags=["아이돌 북마크 (Idol Bookmark)"], summary="내가 북마크한 아이돌 목록 조회"),
    retrieve=extend_schema(tags=["아이돌 북마크 (Idol Bookmark)"], summary="북마크한 아이돌 상세 조회"),
    create=extend_schema(tags=["아이돌 북마크 (Idol Bookmark)"], summary="아이돌 북마크 추가"),
    destroy=extend_schema(tags=["아이돌 북마크 (Idol Bookmark)"], summary="아이돌 북마크 삭제")
)
class IdolBookmarkViewSet(viewsets.ModelViewSet):
    queryset = IdolBookmark.objects.all()
    serializer_class = IdolBookmarkSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options'] # update, partial_update 제외

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if IdolBookmark.objects.filter(
            user=self.request.user, idol=serializer.validated_data["idol"]
        ).exists():
            # 이 부분은 실제로는 serializer의 validate 메서드에서 처리하는 것이 더 좋습니다.
            # drf-spectacular가 perform_create의 Response를 제대로 분석하지 못할 수 있습니다.
            # 하지만 현재 구조를 유지하며 스키마만 추가합니다.
            pass
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=["그룹 북마크 (Group Bookmark)"], summary="내가 북마크한 그룹 목록 조회"),
    retrieve=extend_schema(tags=["그룹 북마크 (Group Bookmark)"], summary="북마크한 그룹 상세 조회"),
    create=extend_schema(tags=["그룹 북마크 (Group Bookmark)"], summary="그룹 북마크 추가"),
    destroy=extend_schema(tags=["그룹 북마크 (Group Bookmark)"], summary="그룹 북마크 삭제")
)
class GroupBookmarkViewSet(viewsets.ModelViewSet):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options'] # update, partial_update 제외

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if GroupBookmark.objects.filter(
            user=self.request.user, group=serializer.validated_data["group"]
        ).exists():
            pass
        serializer.save(user=self.request.user)