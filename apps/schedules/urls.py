from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import IdolScheduleViewSet, GroupScheduleViewSet, UserScheduleViewSet, ManagerScheduleViewSet, ManagerMainboardView

router = DefaultRouter()
router.register(r'idols', IdolScheduleViewSet)
router.register(r'groups', GroupScheduleViewSet)
router.register(r'my', UserScheduleViewSet, basename='my-schedules')
router.register(r'manager', ManagerScheduleViewSet, basename='manager-schedules')

urlpatterns = [
    path('manager/mainboard/', ManagerMainboardView.as_view(), name="manager-mainboard"),
    path('', include(router.urls)),
]