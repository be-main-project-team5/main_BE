from django.contrib import admin
from .models import ChatRoom, ChatMessage, ChatParticipant

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(ChatParticipant)