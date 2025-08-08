from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet

# 이 파일은 'groups' 애플리케이션의 URL 라우팅을 정의합니다.
# Django REST Framework의 DefaultRouter를 사용하여 GroupViewSet에 대한 RESTful API 엔드포인트를 자동으로 생성합니다.
# 이 URL 설정은 'config/urls.py'에서 include되어 전체 프로젝트의 URL 구조에 통합됩니다.

# DefaultRouter는 ViewSet에 대한 표준 라우팅을 자동으로 생성해주는 도구입니다.
# 예를 들어, GroupViewSet에 대해 /groups/ (리스트 및 생성)와 /groups/{pk}/ (상세 조회, 업데이트, 삭제)와 같은 URL 패턴을 자동으로 만들어줍니다.
router = DefaultRouter()

# 'groups'라는 기본 경로(prefix)에 GroupViewSet을 등록합니다.
# 이렇게 등록하면 다음과 같은 URL 패턴이 자동으로 생성됩니다:
# - GET /groups/: 모든 그룹 목록 조회
# - POST /groups/: 새 그룹 생성
# - GET /groups/{id}/: 특정 ID의 그룹 상세 조회
# - PUT /groups/{id}/: 특정 ID의 그룹 전체 업데이트
# - PATCH /groups/{id}/: 특정 ID의 그룹 부분 업데이트
# - DELETE /groups/{id}/: 특정 ID의 그룹 삭제
# GroupViewSet은 'apps/groups/views.py'에 정의되어 있습니다.
router.register(r"", GroupViewSet)

# 'groups' 애플리케이션의 URL 패턴을 정의합니다.
# path('', include(router.urls))는 DefaultRouter가 생성한 모든 URL 패턴을 이 애플리케이션의 루트 경로에 포함시킵니다.
# 예를 들어, 'config/urls.py'에서 path('api/v1/', include('apps.groups.urls'))로 설정되어 있다면,
# 최종적으로 /api/v1/groups/ 와 같은 형태로 접근할 수 있게 됩니다.
urlpatterns = [
    path("", include(router.urls)),
]
