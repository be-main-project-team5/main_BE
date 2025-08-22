from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatParticipant, ChatRoom
from .serializers import ChatMessageSerializer, ChatRoomSerializer, UserSerializer

User = get_user_model()


@extend_schema_view(
    list=extend_schema(tags=["채팅 (Chats)"], summary="내 채팅방 목록 조회"),
    retrieve=extend_schema(tags=["채팅 (Chats)"], summary="채팅방 상세 정보 조회"),
    create=extend_schema(tags=["채팅 (Chats)"], summary="새 채팅방 생성"),
    update=extend_schema(tags=["채팅 (Chats)"], summary="채팅방 정보 수정"),
    partial_update=extend_schema(
        tags=["채팅 (Chats)"], summary="채팅방 정보 부분 수정"
    ),
    destroy=extend_schema(tags=["채팅 (Chats)"], summary="채팅방 삭제"),
    messages=extend_schema(
        tags=["채팅 (Chats)"],
        summary="채팅방 메시지 목록 조회",
        responses=ChatMessageSerializer(many=True),
    ),
    join=extend_schema(tags=["채팅 (Chats)"], summary="채팅방 참여"),
    leave=extend_schema(tags=["채팅 (Chats)"], summary="채팅방 나가기"),
    participants=extend_schema(
        tags=["채팅 (Chats)"],
        summary="채팅방 참여자 목록 조회",
        responses=UserSerializer(many=True),
    ),
)
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants__user=self.request.user
        ).prefetch_related("participants__user", "last_message__sender")

    def perform_create(self, serializer):
        room = serializer.save()
        ChatParticipant.objects.create(room=room, user=self.request.user)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        room = self.get_object()
        messages = room.messages.all().select_related("sender")
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        room = self.get_object()
        participant, created = ChatParticipant.objects.get_or_create(
            room=room, user=request.user
        )
        if created:
            return Response({"status": "user joined"}, status=status.HTTP_201_CREATED)
        return Response({"status": "user already in room"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def leave(self, request, pk=None):
        room = self.get_object()
        try:
            participant = ChatParticipant.objects.get(room=room, user=request.user)
            participant.delete()
            return Response({"status": "user left"}, status=status.HTTP_204_NO_CONTENT)
        except ChatParticipant.DoesNotExist:
            return Response(
                {"error": "User not in room"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        room = self.get_object()
        participants = room.participants.all()
        users = [p.user for p in participants]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@extend_schema(exclude=True)  # 테스트용 HTML 뷰는 API 문서에서 제외
def test_chat_room(request, room_name):
    return render(
        request,
        "chats/testHTML.html",
        {
            "room_name": room_name,
            "user_id": request.user.id,
        },
    )
