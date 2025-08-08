from django.urls import path

from .views import (
    IdolDetailView,
    IdolListView,
    IdolScheduleDetailView,
    IdolScheduleView,
)

urlpatterns = [
    path("idols/", IdolListView.as_view(), name="idol-list"),
    path("idols/<int:idol_id>/", IdolDetailView.as_view(), name="idol-detail"),
    path(
        "idols/<int:idol_id>/schedules/",
        IdolScheduleView.as_view(),
        name="idol-schedule",
    ),
    path(
        "idols/<int:idol_id>/schedules/<int:scheduls_id>",
        IdolScheduleDetailView.as_view(),
        name="idol-schedule-detail",
    ),
]
