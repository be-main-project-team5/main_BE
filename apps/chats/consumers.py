import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ChatMessage, ChatRoom

# Django의 현재 활성화된 사용자 모델을 가져옵니다.
User = get_user_model()


# ChatConsumer: 웹소켓 연결을 처리하고 실시간 메시지 통신을 구현하는 Consumer입니다.
# AsyncWebsocketConsumer를 상속받아 비동기적으로 동작합니다.
# 연동: apps/chats/routing.py를 통해 웹소켓 URL과 연결됩니다.
# 기능: 웹소켓 연결/해제, 클라이언트로부터 메시지 수신, 데이터베이스 저장, 다른 클라이언트로 메시지 브로드캐스트를 담당합니다.
class ChatConsumer(AsyncWebsocketConsumer):
    # connect: 클라이언트가 웹소켓에 연결될 때 호출됩니다.
    async def connect(self):
        # URL 경로에서 room_name을 추출합니다 (예: ws/chats/1/ 에서 '1').
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # 채널 레이어 그룹 이름을 정의합니다 (예: 'chat_1').
        self.room_group_name = f"chat_{self.room_name}"

        # 채널 레이어의 그룹에 현재 채널을 추가합니다.
        # 이렇게 하면 같은 그룹에 속한 모든 채널에 메시지를 보낼 수 있습니다.
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # 웹소켓 연결을 수락합니다.
        await self.accept()

    # disconnect: 클라이언트가 웹소켓 연결을 끊을 때 호출됩니다.
    async def disconnect(self, close_code):
        # 채널 레이어의 그룹에서 현재 채널을 제거합니다.
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # receive: 클라이언트로부터 웹소켓 메시지를 수신할 때 호출됩니다.
    async def receive(self, text_data):
        # 수신된 텍스트 데이터를 JSON으로 파싱합니다.
        text_data_json = json.loads(text_data)
        # 메시지 내용을 추출합니다.
        message = text_data_json["message"]
        # 현재 연결된 사용자의 ID를 가져옵니다. (인증 미구현 시 AnonymousUser일 수 있음)
        sender_id = self.scope["user"].id

        # 메시지를 데이터베이스에 저장합니다.
        # database_sync_to_async 데코레이터로 동기 ORM 작업을 비동기 컨텍스트에서 실행합니다.
        await self.save_message(sender_id, self.room_name, message)

        # 같은 그룹에 속한 모든 채널(클라이언트)에게 메시지를 브로드캐스트합니다.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # 이 타입은 아래 chat_message 메서드를 호출합니다.
                "message": message,
                "sender_id": sender_id,
            },
        )

    # chat_message: 채널 레이어 그룹으로부터 메시지를 수신할 때 호출됩니다.
    # 이 메서드는 group_send에서 "type": "chat_message"로 지정되었을 때 실행됩니다.
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        # 발신자 정보를 데이터베이스에서 비동기적으로 가져옵니다.
        sender = await self.get_user(sender_id)

        # 수신된 메시지를 웹소켓을 통해 클라이언트에게 다시 보냅니다.
        # 클라이언트 측에서는 이 JSON 데이터를 파싱하여 메시지를 화면에 표시합니다.
        await self.send(
            text_data=json.dumps({"message": message, "sender": sender.nickname})
        )

    # save_message: 메시지를 데이터베이스에 저장하는 동기 함수를 비동기 컨텍스트에서 실행합니다.
    @database_sync_to_async
    def save_message(self, sender_id, room_name, message):
        # room_name은 실제로는 room_id입니다.
        room = ChatRoom.objects.get(id=room_name)
        sender = User.objects.get(id=sender_id)
        ChatMessage.objects.create(room=room, sender=sender, content=message)

    # get_user: 사용자 ID로 User 객체를 가져오는 동기 함수를 비동기 컨텍스트에서 실행합니다.
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
