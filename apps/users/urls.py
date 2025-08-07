from django.urls import path

from .views import (
    UserDeleteView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserSignupView,
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("delete/", UserDeleteView.as_view(), name="delete"),
]
