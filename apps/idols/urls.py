from django.urls import path

from .views import (
    IdolDetailView,
    IdolListView,
    IdolScheduleDetailView,
    IdolScheduleView,
    IdolMainboardView,
)

urlpatterns = [
    path("mainboard/", IdolMainboardView.as_view(), name="idol-mainboard"),
    path("", IdolListView.as_view(), name="idol-list"),
    path("<int:idol_id>/", IdolDetailView.as_view(), name="idol-detail"),
    path("<int:idol_id>/schedules/",IdolScheduleView.as_view(), name="idol-schedule"),
    path("<int:idol_id>/schedules/<int:scheduls_id>/", IdolScheduleDetailView.as_view(), name="idol-schedule-detail",)
]
