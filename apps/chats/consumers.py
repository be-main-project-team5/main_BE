import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import ChatMessage, ChatRoom
from .serializers import ChatMessageSerializer, ChatRoomSerializer  # 새로 추가

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        if not self.user_authenticated():
            await self.close(code=4001)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 연결 시 채팅방의 최신 상태를 전송
        chat_room = await self.get_chat_room_with_details(self.room_id)
        serializer = ChatRoomSerializer(chat_room)
        await self.send(
            text_data=json.dumps(
                {"type": "chat_room_initial_state", "chat_room": serializer.data}
            )
        )

    def user_authenticated(self):
        user = self.scope.get("user", None)
        if isinstance(user, AnonymousUser) or not user:
            return False
        return True

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message_content = text_data_json["message"]
    #     sender_id = self.scope["user"].id

    #     # 메시지 저장 및 ChatRoom.last_message 업데이트
    #     message_obj = await self.save_message(sender_id, self.room_id, message_content)

    #     # 업데이트된 ChatRoom 객체 가져오기 (last_message와 participants 프리페치)
    #     chat_room = await self.get_chat_room_with_details(self.room_id)

    #     # ChatRoom 객체 직렬화
    #     serializer = ChatRoomSerializer(chat_room)
    #     serialized_data = serializer.data

    #     # 직렬화된 ChatRoom 데이터를 그룹에 전송
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             "type": "chat_room_update",  # 프론트엔드에서 구분할 새로운 타입
    #             "chat_room": serialized_data,
    #         },
    #     )

    async def receive(self, text_data=None, bytes_data=None):
        """
        클라이언트에서 메시지 수신 시 실행됨
        """
        data = json.loads(text_data)

        message_type = data.get("type")

        # 일반 채팅 메시지 처리
        if message_type == "chat.message":
            message = data.get("message")

            # 그룹 전체에 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user": str(self.scope["user"]),
                }
            )

    @database_sync_to_async
    def save_message(self, sender_id, room_id, message_content):
        room = ChatRoom.objects.get(id=room_id)
        sender = User.objects.get(id=sender_id)
        message = ChatMessage.objects.create(
            room=room, sender=sender, content=message_content
        )
        room.last_message = message
        room.save()
        return message

    @database_sync_to_async
    def get_chat_room_with_details(self, room_id):
        # ChatRoom 객체를 가져오면서 last_message와 participants를 프리페치
        return (
            ChatRoom.objects.select_related("last_message__sender")
            .prefetch_related("participants__user")
            .get(id=room_id)
        )