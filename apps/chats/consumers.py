import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatMessage, ChatRoom

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # if not self.scope["user"].is_authenticated:
        #     await self.close()
        #     return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        history = await self.get_chat_history(self.room_name)
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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        sender_id = self.scope["user"].id

        message_obj = await self.save_message(
            sender_id, self.room_name, message_content
        )

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
    def save_message(self, sender_id, room_name, message_content):
        room = ChatRoom.objects.get(id=room_name)
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
    def get_chat_history(self, room_name):
        messages = (
            ChatMessage.objects.filter(room__id=room_name)
            .order_by("sent_at")
            .values("content", "sender__nickname", "sent_at", "sender_id")
        )
        return list(messages)
