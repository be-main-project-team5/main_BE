from datetime import date

import requests
from django.conf import settings
from django.db import transaction
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.bookmarks.models import GroupBookmark, IdolBookmark
from apps.schedules.models import GroupSchedule, IdolSchedule, UserSchedule

from .models import CustomUser
from .serializers import (
    FanMainboardSerializer,
    PasswordChangeSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserSignupSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# 사용자 생성 View
class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response(
                {
                    "message": "회원가입이 성공적으로 완료되었습니다.",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            if "email" in e.detail and "conflict" in e.detail["email"][0].code:
                return Response(
                    {"email": e.detail["email"]}, status=status.HTTP_409_CONFLICT
                )
            if "nickname" in e.detail and "conflict" in e.detail["nickname"][0].code:
                return Response(
                    {"nickname": e.detail["nickname"]}, status=status.HTTP_409_CONFLICT
                )
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {
                    "detail": f"서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요. ({str(e)})"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 사용자 로그인 View
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        tokens = get_tokens_for_user(user)

        profile_image_url = None
        if user.profile_image:
            profile_image_url = user.profile_image.url

        return Response(
            {
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "profile_image_url": profile_image_url,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


# 사용자 로그아웃 View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response(
                {"message": "성공적으로 로그아웃되었습니다."},
                status=status.HTTP_204_NO_CONTENT,
            )
            response.set_cookie(
                "refresh_token",
                value="",
                httponly=True,
                secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
                samesite="Lax",
                max_age=0,
            )
            return response
        except TokenError as e:
            return Response(
                data={"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"로그아웃 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MyPageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"사용자 정보를 조회하는 중 오류가 발생했습니다. ({str(e)})"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "회원 정보가 성공적으로 수정되었습니다.",
                    "updated_profile": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            if "nickname" in e.detail and "conflict" in e.detail["nickname"][0].code:
                return Response(
                    {"nickname": e.detail["nickname"]}, status=status.HTTP_409_CONFLICT
                )
        except Exception as e:
            return Response(
                {"detail": f"회원 정보 수정 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            password = request.data.get("password")
            if not password:
                raise ValidationError({"password": "비밀번호를 입력해주세요."})

            user = self.get_object()
            if not user.check_password(password):
                raise ValidationError({"password": "비밀번호가 일치하지 않습니다."})

            with transaction.atomic():
                user.is_active = False
                user.save()

            return Response(
                {"message": "회원 탈퇴가 성공적으로 완료되었습니다."},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"회원 탈퇴 처리 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_password = request.data.get("current_password")
        if not current_password:
            return Response(
                {"error": "현재 비밀번호를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.user.check_password(current_password):
            return Response(
                {"error": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {"message": "비밀번호가 확인되었습니다."},
            status=status.HTTP_200_OK,
        )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            serializer = PasswordChangeSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response(
                {"message": "비밀번호가 성공적으로 변경되었습니다."},
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"비밀번호 변경 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FanMainboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()

        bookmarked_idols = IdolBookmark.objects.filter(user=user).values_list(
            "idol_id", flat=True
        )
        bookmarked_groups = GroupBookmark.objects.filter(user=user).values_list(
            "group_id", flat=True
        )

        idol_schedules = IdolSchedule.objects.filter(
            idol_id__in=bookmarked_idols, start_time__date=today
        )
        group_schedules = GroupSchedule.objects.filter(
            group_id__in=bookmarked_groups, start_time__date=today
        )

        user_schedules = UserSchedule.objects.filter(
            user=user, idol_schedule__start_time__date=today
        ).select_related("idol_schedule")
        user_group_schedules = UserSchedule.objects.filter(
            user=user, group_schedule__start_time__date=today
        ).select_related("group_schedule")

        all_schedules = list(idol_schedules) + list(group_schedules)
        all_schedules += [us.idol_schedule for us in user_schedules if us.idol_schedule]
        all_schedules += [
            ugs.group_schedule for ugs in user_group_schedules if ugs.group_schedule
        ]

        all_schedules = list(set(all_schedules))

        serializer = FanMainboardSerializer(all_schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            code = request.GET.get("code")
            if not code:
                return Response(
                    {"error": "Authorization code not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token_response = requests.post(
                "https://kauth.kakao.com/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "client_id": settings.KAKAO_REST_API_KEY,
                    "redirect_uri": settings.KAKAO_REDIRECT_URI,
                    "code": code,
                },
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                timeout=5,
            )

            token_json = token_response.json()
            if "error" in token_json:
                return Response(
                    {
                        "error": token_json["error"],
                        "error_description": token_json.get("error_description"),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            access_token = token_json.get("access_token")
            if not access_token:
                return Response(
                    {"error": "Failed to retrieve access token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_info_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
                timeout=5,
            )
            user_info = user_info_response.json()

            kakao_id = user_info.get("id")
            email = user_info.get("kakao_account", {}).get("email")
            nickname = user_info.get("properties", {}).get("nickname")
            if not email:
                email = f"{kakao_id}@kakao.user"

            if not kakao_id:
                return Response(
                    {"error": "Failed to get user information from Kakao."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user, created = CustomUser.objects.get_or_create(
                social_id=str(kakao_id),
                social_provider="kakao",
                defaults={"email": email, "nickname": nickname, "is_active": True},
            )

            if not created:
                if email and user.email != email:
                    user.email = email
                if nickname and user.nickname != nickname:
                    user.nickname = nickname
                user.save()

            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)

        except requests.Timeout:
            return Response(
                {"error": "External service timeout."},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            code = request.GET.get("code")
            if not code:
                return Response(
                    {"error": "Authorization code not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": "http://127.0.0.1:8000/api/v1/users/google/callback/",
                    "grant_type": "authorization_code",
                },
            )

            token_json = token_response.json()
            if "error" in token_json:
                return Response(
                    {"error": token_json["error"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            access_token = token_json.get("access_token")

            user_info_response = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            user_info = user_info_response.json()
            google_id = user_info.get("id")
            email = user_info.get("email")
            nickname = user_info.get("name")

            if not google_id:
                return Response(
                    {"error": "Failed to get user information from Google."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user, created = CustomUser.objects.get_or_create(
                social_id=str(google_id),
                social_provider="google",
                defaults={
                    "email": email,
                    "nickname": nickname,
                    "is_active": True,
                },
            )

            if not created:
                if email and user.email != email:
                    user.email = email
                if nickname and user.nickname != nickname:
                    user.nickname = nickname
                user.save()

            tokens = get_tokens_for_user(user)

            return Response(tokens, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
