from django.urls import path
from rest_framework_nested import routers

from .views import GroupMembersView, GroupViewSet

# 'groups'라는 기본 경로(prefix)에 GroupViewSet을 등록합니다.
# 이렇게 등록하면 다음과 같은 URL 패턴이 자동으로 생성됩니다:
# - GET /groups/: 모든 그룹 목록 조회
# - POST /groups/: 새 그룹 생성
# - GET /groups/{id}/: 특정 ID의 그룹 상세 조회
# - PUT /groups/{id}/: 특정 ID의 그룹 전체 업데이트
# - PATCH /groups/{id}/: 특정 ID의 그룹 부분 업데이트
# - DELETE /groups/{id}/: 특정 ID의 그룹 삭제
# GroupViewSet은 'apps/groups/views.py'에 정의되어 있습니다.

# 1. 기본 라우터 생성
router = routers.DefaultRouter()
router.register(r"", GroupViewSet, basename="group")

urlpatterns = router.urls

# 그룹 구성원 조회를 위한 URL 추가
urlpatterns += [
    path("members/", GroupMembersView.as_view(), name="group-members"),
]