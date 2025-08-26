import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import ChatMessage, ChatRoom
from .serializers import ChatRoomSerializer  # 새로 추가
from .serializers import ChatMessageSerializer

User = get_user_model()

# 기존의 ChatConsumer
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
#         self.room_group_name = f"chat_{self.room_id}"

#         if not self.user_authenticated():
#             await self.close(code=4001)

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#         # 연결 시 채팅방의 최신 상태를 전송
#         chat_room = await self.get_chat_room_with_details(self.room_id)
#         serializer = ChatRoomSerializer(chat_room)
#         await self.send(
#             text_data=json.dumps(
#                 {"type": "chat_room_initial_state", "chat_room": serializer.data}
#             )
#         )

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        웹소켓 연결 시 실행
        """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # 그룹 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # 채팅방 초기 상태 전송
        chat_room_data = await self.get_chat_room_data(self.room_name)
        await self.send(text_data=json.dumps({
            "type": "chat_room.initial_state",
            "chat_room": chat_room_data,
        }))

    async def disconnect(self, close_code):
        """
        연결 종료 시 실행
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        클라이언트에서 메시지 수신
        """
        data = json.loads(text_data)
        message_content = data.get("content")
        sender_id = data.get("sender_id")

        # DB 저장
        message_data = await self.save_message(
            room_name=self.room_name,
            sender_id=sender_id,
            content=message_content
        )

        # (1) 보낸 사람에게 응답 → "내가 보낸 메시지 저장 완료됨" 알림
        await self.send(text_data=json.dumps({
            "type": "chat.message.sent",
            "message": message_data,
        }))

        # (2) 그룹에 전파 → 모든 클라이언트가 새 메시지 수신
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message_broadcast",
                "message": message_data,
            }
        )

    async def chat_message_broadcast(self, event):
        """
        그룹 메시지 전파
        """
        await self.send(text_data=json.dumps({
            "type": "chat.message.broadcast",
            "message": event["message"],
        }))

    def user_authenticated(self):
        user = self.scope.get("user", None)
        if isinstance(user, AnonymousUser) or not user:
            return False
        return True

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        sender_id = self.scope["user"].id

        # 메시지 저장 및 ChatRoom.last_message 업데이트
        message_obj = await self.save_message(sender_id, self.room_id, message_content)

        # 업데이트된 ChatRoom 객체 가져오기 (last_message와 participants 프리페치)
        chat_room = await self.get_chat_room_with_details(self.room_id)

        # ChatRoom 객체 직렬화
        serializer = ChatRoomSerializer(chat_room)
        serialized_data = serializer.data

        # 직렬화된 ChatRoom 데이터를 그룹에 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_room_update",  # 프론트엔드에서 구분할 새로운 타입
                "chat_room": serialized_data,
            },
        )

    # 기존의 chat_message, get_user, get_user_nickname, get_chat_history 메서드는 더 이상 필요 없으므로 제거
    # async def chat_message(self, event):
    #     await self.send(
    #         text_data=json.dumps(
    #             {
    #                 "message": event["message"],
    #                 "sender": event["sender"],
    #                 "sent_at": event["sent_at"],
    #                 "sender_id": event["sender_id"],
    #             }
    #         )
    #     )

    @database_sync_to_async
    def get_chat_room_data(self, room_name):
        chat_room = ChatRoom.objects.get(name=room_name)
        serializer = ChatRoomSerializer(chat_room)
        return serializer.data

    @database_sync_to_async
    def save_message(self, room_name, sender_id, content):
        chat_room = ChatRoom.objects.get(name=room_name)
        message = ChatMessage.objects.create(
            chat_room=chat_room,
            sender_id=sender_id,
            content=content,
            sent_at=timezone.now(),
        )
        serializer = ChatMessageSerializer(message)
        return serializer.data

    # 기존의 DB Helpers
    # @database_sync_to_async
    # def save_message(self, sender_id, room_id, message_content):
    #     room = ChatRoom.objects.get(id=room_id)
    #     sender = User.objects.get(id=sender_id)
    #     message = ChatMessage.objects.create(
    #         room=room, sender=sender, content=message_content
    #     )
    #     # Update last_message of the ChatRoom
    #     room.last_message = message
    #     room.save()
    #     return message

    # @database_sync_to_async
    # def get_chat_room_with_details(self, room_id):
    #     # ChatRoom 객체를 가져오면서 last_message와 participants를 프리페치
    #     return (
    #         ChatRoom.objects.select_related("last_message__sender")
    #         .prefetch_related("participants__user")
    #         .get(id=room_id)
    #     )
