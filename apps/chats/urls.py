from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# DefaultRouter를 사용하여 ViewSet에 대한 URL 패턴을 자동으로 생성합니다.
router = DefaultRouter()
# 'rooms' 경로에 ChatRoomViewSet을 등록합니다.
# basename='chatroom': URL 패턴의 이름을 지정합니다 (예: chatroom-list, chatroom-detail).
# 이 등록으로 다음과 같은 URL이 자동으로 생성됩니다:
# - /rooms/ (GET, POST) -> ChatRoomViewSet.list(), ChatRoomViewSet.create()
# - /rooms/{pk}/ (GET, PUT, PATCH, DELETE) -> ChatRoomViewSet.retrieve(), update(), partial_update(), destroy()
# - /rooms/{pk}/messages/ (GET) -> ChatRoomViewSet.messages()
# - /rooms/{pk}/join/ (POST) -> ChatRoomViewSet.join()
# - /rooms/{pk}/leave/ (POST) -> ChatRoomViewSet.leave()
# - /rooms/{pk}/participants/ (GET) -> ChatRoomViewSet.participants()
router.register(r"rooms", views.ChatRoomViewSet, basename="chatroom")

# 앱의 URL 패턴을 정의합니다.
# include(router.urls): DefaultRouter가 생성한 모든 URL 패턴을 포함합니다.
urlpatterns = [
    path("", include(router.urls)),
    # 테스트용 채팅방 페이지를 위한 URL
    path("test/<str:room_name>/", views.test_chat_room, name="test_chat_room"),
]
