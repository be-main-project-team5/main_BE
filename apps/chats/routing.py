from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/chats/<int:room_id>/", consumers.ChatConsumer.as_asgi()),
]