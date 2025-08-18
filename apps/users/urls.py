from django.urls import path

from .views import (
    FanMainboardView,
    GoogleCallbackView,
    KakaoCallbackView,
    MyPageView,
    PasswordChangeView,
    PasswordVerifyView,
    UserLoginView,
    UserLogoutView,
    UserSignupView,
)

urlpatterns = [
    path("mainboard/", FanMainboardView.as_view(), name="mainboard"),
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("password/verify/", PasswordVerifyView.as_view(), name="password-verify"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("kakao/callback/", KakaoCallbackView.as_view(), name="kakao-callback"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google-callback"),
]