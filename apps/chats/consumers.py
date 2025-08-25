import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .models import ChatMessage, ChatRoom

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        if not self.user_authenticated():
            await self.close(code=4001)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        history = await self.get_chat_history(self.room_id)
        for message in history:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message["content"],
                        "sender": message["sender__nickname"],
                        "sent_at": message["sent_at"].isoformat(),
                        "sender_id": message["sender_id"],
                    }
                )
            )
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

        message_obj = await self.save_message(sender_id, self.room_id, message_content)

        sender_nickname = await self.get_user_nickname(sender_id)
        sent_at = message_obj.sent_at.isoformat()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "sender": sender_nickname,
                "sent_at": sent_at,
                "sender_id": sender_id,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                    "sent_at": event["sent_at"],
                    "sender_id": event["sender_id"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, sender_id, room_id, message_content):
        room = ChatRoom.objects.get(id=room_id)
        sender = User.objects.get(id=sender_id)
        return ChatMessage.objects.create(
            room=room, sender=sender, content=message_content
        )

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_user_nickname(self, user_id):
        return User.objects.get(id=user_id).nickname

    @database_sync_to_async
    def get_chat_history(self, room_id):
        messages = (
            ChatMessage.objects.filter(room__id=room_id)
            .order_by("sent_at")
            .values("content", "sender__nickname", "sent_at", "sender_id")
        )
        return list(messages)
