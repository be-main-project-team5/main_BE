from rest_framework_nested import routers
from .views import GroupViewSet, GroupScheduleViewSet

# 1. 기본 라우터 생성
router = routers.DefaultRouter()
router.register(r'', GroupViewSet, basename='group')

# 2. groups 라우터에 중첩될 schedules 라우터 생성
schedules_router = routers.NestedDefaultRouter(router, r'', lookup='group')

# 3. 중첩 라우터에 schedules ViewSet 등록
schedules_router.register(r'schedules', GroupScheduleViewSet, basename='group-schedules')

# 4. urlpatterns에 두 라우터의 URL을 모두 포함
urlpatterns = router.urls + schedules_router.urls