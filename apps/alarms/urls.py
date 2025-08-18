from django.urls import path

from .views import AlarmCreateView, AlarmDetailView, AlarmListView

urlpatterns = [
    path("", AlarmListView.as_view(), name="alarm-list"),
    path("create/", AlarmCreateView.as_view(), name="alarm-create"),
    path("<int:id>/", AlarmDetailView.as_view(), name="alarm-detail"),
]
