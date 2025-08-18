from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "admins_api"

router = DefaultRouter()
router.register(r'managers', views.IdolManagerViewSet, basename='idolmanager')

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDeleteView.as_view(), name="user_delete"),
    path("create-manager/", views.ManagerCreateView.as_view(), name="create_manager"),
    path("create-idol/", views.IdolCreateView.as_view(), name="create_idol"),
] + router.urls