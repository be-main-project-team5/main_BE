from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GroupBookmark, IdolBookmark
from .serializers import GroupBookmarkSerializer, IdolBookmarkSerializer


class IdolBookmarkViewSet(viewsets.ModelViewSet):
    queryset = IdolBookmark.objects.all()
    serializer_class = IdolBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 중복 북마크 방지
        if IdolBookmark.objects.filter(
            user=self.request.user, idol=serializer.validated_data["idol"]
        ).exists():
            return Response(
                {"detail": "이미 북마크된 아이돌입니다."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer.save(user=self.request.user)


class GroupBookmarkViewSet(viewsets.ModelViewSet):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 중복 북마크 방지
        if GroupBookmark.objects.filter(
            user=self.request.user, group=serializer.validated_data["group"]
        ).exists():
            return Response(
                {"detail": "이미 북마크된 그룹입니다."}, status=status.HTTP_409_CONFLICT
            )
        serializer.save(user=self.request.user)
