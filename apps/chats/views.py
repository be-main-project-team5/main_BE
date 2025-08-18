from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import ChatParticipant, ChatRoom
from .serializers import ChatMessageSerializer, ChatRoomSerializer, UserSerializer

# Django의 현재 활성화된 사용자 모델을 가져옵니다.
User = get_user_model()


# ChatRoomViewSet: ChatRoom 모델에 대한 RESTful API 뷰셋을 정의합니다.
# 연동: apps/chats/urls.py를 통해 URL과 연결되며, apps/chats/serializers.py를 사용하여 데이터를 직렬화합니다.
# 기능: 채팅방 목록 조회, 생성, 상세 조회, 메시지 조회, 참여/나가기, 참여자 목록 조회 등의 기능을 제공합니다.
class ChatRoomViewSet(viewsets.ModelViewSet):
    # 기본 쿼리셋 (모든 채팅방).
    queryset = ChatRoom.objects.all()
    # 이 뷰셋에서 사용할 기본 시리얼라이저.
    serializer_class = ChatRoomSerializer

    # get_queryset: 현재 요청을 보낸 사용자가 참여하고 있는 채팅방만 반환하도록 쿼리셋을 오버라이드합니다.
    # prefetch_related: N+1 쿼리 문제를 방지하기 위해 관련 객체들을 미리 가져옵니다.
    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants__user=self.request.user
        ).prefetch_related("participants__user", "last_message__sender")

    # perform_create: 채팅방 생성 시 추가 로직을 수행합니다.
    # serializer.save(): ChatRoom 인스턴스를 생성하고 저장합니다.
    # ChatParticipant.objects.create(): 채팅방 생성 후, 현재 요청을 보낸 사용자를 해당 채팅방의 참여자로 자동 추가합니다.
    def perform_create(self, serializer):
        room = serializer.save()
        ChatParticipant.objects.create(room=room, user=self.request.user)

    # @action(detail=True, methods=['get']): 특정 채팅방(detail=True)에 대한 GET 요청을 처리하는 커스텀 액션입니다.
    # URL: /api/v1/chats/rooms/{pk}/messages/
    # 기능: 해당 채팅방의 모든 메시지를 조회하여 반환합니다.
    def messages(self, request, pk=None):
        room = self.get_object()  # 현재 요청된 채팅방 객체를 가져옵니다.
        messages = room.messages.all().select_related(
            "sender"
        )  # 해당 채팅방의 모든 메시지를 가져오고, 발신자 정보를 미리 로드합니다.
        serializer = ChatMessageSerializer(
            messages, many=True
        )  # 메시지 목록을 직렬화합니다.
        return Response(serializer.data)

    # @action(detail=True, methods=['post']): 특정 채팅방에 대한 POST 요청을 처리하는 커스텀 액션입니다.
    # URL: /api/v1/chats/rooms/{pk}/join/
    # 기능: 현재 요청을 보낸 사용자를 해당 채팅방에 참여시킵니다.
    def join(self, request, pk=None):
        room = self.get_object()
        # get_or_create: 해당 방에 사용자가 이미 참여하고 있으면 기존 객체를, 없으면 새로 생성합니다.
        participant, created = ChatParticipant.objects.get_or_create(
            room=room, user=request.user
        )
        if created:
            # 새로 참여한 경우 201 Created 응답
            return Response({"status": "user joined"}, status=status.HTTP_201_CREATED)
        # 이미 참여하고 있는 경우 200 OK 응답
        return Response({"status": "user already in room"}, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['post']): 특정 채팅방에 대한 POST 요청을 처리하는 커스텀 액션입니다.
    # URL: /api/v1/chats/rooms/{pk}/leave/
    # 기능: 현재 요청을 보낸 사용자를 해당 채팅방에서 나가게 합니다.
    def leave(self, request, pk=None):
        room = self.get_object()
        try:
            # 해당 방에서 사용자의 참여자 정보를 찾아 삭제합니다.
            participant = ChatParticipant.objects.get(room=room, user=request.user)
            participant.delete()
            # 성공적으로 나간 경우 204 No Content 응답
            return Response({"status": "user left"}, status=status.HTTP_204_NO_CONTENT)
        except ChatParticipant.DoesNotExist:
            # 참여자 정보가 없는 경우 404 Not Found 응답
            return Response(
                {"error": "User not in room"}, status=status.HTTP_404_NOT_FOUND
            )

    # @action(detail=True, methods=['get']): 특정 채팅방에 대한 GET 요청을 처리하는 커스텀 액션입니다.
    # URL: /api/v1/chats/rooms/{pk}/participants/
    # 기능: 해당 채팅방의 모든 참여자 목록을 조회하여 반환합니다.
    def participants(self, request, pk=None):
        room = self.get_object()
        participants = (
            room.participants.all()
        )  # 해당 채팅방의 모든 ChatParticipant 객체를 가져옵니다.
        users = [
            p.user for p in participants
        ]  # 각 ChatParticipant에서 User 객체만 추출합니다.
        serializer = UserSerializer(users, many=True)  # User 객체 목록을 직렬화합니다.
        return Response(serializer.data)


def test_chat_room(request, room_name):
    return render(request, "chats/testHTML.html", {"room_name": room_name})
