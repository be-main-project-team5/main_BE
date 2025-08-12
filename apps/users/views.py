from datetime import date

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
    UserDeleteSerializer,
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
    # 누구나 접근 가능
    permission_classes = (AllowAny,)
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()  # Serializer의 create 메서드 호출

            return Response(
                {
                    "message": "회원가입이 성공적으로 완료되었습니다.",
                    "user_id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # Serializer에서 발생한 유효성 검사 오류 처리
            # 이메일 중복 오류
            if "email" in e.detail and "conflict" in e.detail["email"][0].code:
                return Response(
                    {"email": e.detail["email"]}, status=status.HTTP_409_CONFLICT
                )
            # 닉네임 중복 오류
            if "nickname" in e.detail and "conflict" in e.detail["nickname"][0].code:
                return Response(
                    {"nickname": e.detail["nickname"]}, status=status.HTTP_409_CONFLICT
                )
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 기타 예상치 못한 서버 오류 처리
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
    permission_classes = [AllowAny]  # 누구나 접근 가능

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # JWT 토큰 발급
        tokens = get_tokens_for_user(user)

        # 프로필 이미지 URL
        # 프로필사진이 등록된 회원이 로그인하는 경우 바디에 프로필 url을 담아서 보내준다
        profile_image_url = None
        if user.profile_image:
            profile_image_url = user.profile_image.url

        return Response(
            {
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "profile_image_url": profile_image_url,  # 프로필 이미지 URL 추가
                "role": user.role, # 역할 정보 추가
            },
            status=status.HTTP_200_OK,
        )


# 사용자 로그아웃 View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")

            # SimpleJWT가 앱 수준에서 HTTP_401_UNAUTHORIZED 에러 내줌
            # error: Authentication credentials were not provided
            # error: token_not_valid
            # "code": "user_not_found"
            #
            # 이상한 토큰이나 만료된 토큰이면, HTTP_400_BAD_REQUEST
            # error: Token is blacklisted
            #
            # if not refresh_token:
            #     return Response(
            #         {"error": "Refresh token이 제공되지 않았습니다."},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

            token = RefreshToken(refresh_token)
            token.blacklist()  # refresh token을 블랙리스트에 추가

            response = Response(
                {"message": "성공적으로 로그아웃되었습니다."},
                status=status.HTTP_204_NO_CONTENT,  # HTTP_204_NO_CONTENT로 변경
            )
            response.set_cookie(
                "refresh_token",
                value="",
                httponly=True,
                secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
                samesite="Lax",
                max_age=0,  # 만료 시간을 0으로 설정하여 즉시 삭제
            )
            return response
        except TokenError as e:
            return Response(
                data={"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # 그 외 예상치 못한 에러
            return Response(
                {"error": f"로그아웃 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def get_object(self):
        # 현재 로그인한 사용자 객체를 반환
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
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )  # partial=True로 부분 업데이트 허용
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
            # 닉네임 중복 오류 처리
            if "nickname" in e.detail and "conflict" in e.detail["nickname"][0].code:
                return Response(
                    {"nickname": e.detail["nickname"]}, status=status.HTTP_409_CONFLICT
                )
        except Exception as e:
            return Response(
                {"detail": f"회원 정보 수정 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

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
            # 비밀번호 불일치, 유효성 검사 실패 오류 처리
            if (
                "current_password" in e.detail
                and "password_mismatch" in e.detail["current_password"][0].code
            ):
                return Response(
                    {"current_password": e.detail["current_password"]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"비밀번호 변경 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserDeleteSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            user = request.user
            with transaction.atomic():
                # 사용자를 비활성화
                user.is_active = False
                user.save()

                RefreshToken.for_user(user).blacklist()

            return Response(
                {"message": "회원 탈퇴가 성공적으로 완료되었습니다."},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # 비밀번호 불일치 오류 처리
            if (
                "password" in e.detail
                and "password_mismatch" in e.detail["password"][0].code
            ):
                return Response(
                    {"password": e.detail["password"]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"회원 탈퇴 처리 중 오류가 발생했습니다. ({str(e)})"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FanMainboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()

        # Get bookmarked idols and groups
        bookmarked_idols = IdolBookmark.objects.filter(user=user).values_list("idol_id", flat=True)
        bookmarked_groups = GroupBookmark.objects.filter(user=user).values_list("group_id", flat=True)

        # Get schedules for bookmarked idols and groups for today
        idol_schedules = IdolSchedule.objects.filter(idol_id__in=bookmarked_idols, start_time__date=today)
        group_schedules = GroupSchedule.objects.filter(group_id__in=bookmarked_groups, start_time__date=today)

        # Get user's favorited schedules for today
        user_schedules = UserSchedule.objects.filter(user=user, idol_schedule__start_time__date=today).select_related('idol_schedule')
        user_group_schedules = UserSchedule.objects.filter(user=user, group_schedule__start_time__date=today).select_related('group_schedule')

        # Combine all schedules
        all_schedules = list(idol_schedules) + list(group_schedules)
        all_schedules += [us.idol_schedule for us in user_schedules if us.idol_schedule]
        all_schedules += [ugs.group_schedule for ugs in user_group_schedules if ugs.group_schedule]

        # Remove duplicates
        all_schedules = list(set(all_schedules))

        serializer = FanMainboardSerializer(all_schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
