from django.contrib import admin

from .models import ChatMessage, ChatParticipant, ChatRoom

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(ChatParticipant)
