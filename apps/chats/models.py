from django.conf import settings
from django.db import models


# ChatRoom 모델: 개별 채팅방을 나타냅니다.
# 연동: ChatParticipant, ChatMessage 모델과 ForeignKey 관계로 연동됩니다.
# 기능: 채팅방의 기본 정보(이름, 마지막 메시지, 생성/수정 시간)를 저장합니다.
class ChatRoom(models.Model):
    # last_message: 해당 채팅방의 마지막 메시지를 참조합니다.
    # SET_NULL: 참조하는 ChatMessage가 삭제되어도 ChatRoom은 유지됩니다.
    # null=True, blank=True: 마지막 메시지가 없을 수도 있습니다 (예: 새로 생성된 방).
    # related_name='+': 역참조 이름을 생성하지 않아도 됩니다. (순환 참조 방지)
    last_message = models.ForeignKey(
        "ChatMessage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    # room_name: 채팅방의 이름 (예: '카리나-매니저 채팅방').
    # blank=True, null=True: 방 이름이 필수가 아닐 수 있습니다.
    room_name = models.CharField(max_length=255, blank=True, null=True)
    # created_at: 채팅방 생성 시간 (자동으로 현재 시간 기록).
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at: 채팅방 마지막 업데이트 시간 (자동으로 업데이트).
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 데이터베이스 테이블 이름 설정
        db_table = "chat_rooms"
        # 관리자 페이지 등에서 표시될 단수 이름
        verbose_name = "채팅방"
        # 관리자 페이지 등에서 표시될 복수 이름
        verbose_name_plural = "채팅방들"


# ChatParticipant 모델: 어떤 사용자가 어떤 채팅방에 참여하고 있는지 기록합니다.
# 연동: ChatRoom, User 모델과 ForeignKey 관계로 연동됩니다.
# 기능: 채팅방과 사용자 간의 다대다(M:N) 관계를 정의하고, 참여 시간을 기록합니다.
class ChatParticipant(models.Model):
    # room: 참여자가 속한 ChatRoom을 참조합니다.
    # CASCADE: 참조하는 ChatRoom이 삭제되면 참여자 정보도 함께 삭제됩니다.
    # related_name='participants': ChatRoom 객체에서 이 참여자들을 역참조할 때 사용합니다 (예: room.participants.all()).
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="participants"
    )
    # user: 참여하는 사용자를 참조합니다.
    # settings.AUTH_USER_MODEL: Django의 현재 활성화된 사용자 모델을 참조합니다 (CustomUser).
    # CASCADE: 참조하는 User가 삭제되면 참여자 정보도 함께 삭제됩니다.
    # related_name='chat_rooms': User 객체에서 이 사용자가 참여한 채팅방들을 역참조할 때 사용합니다 (예: user.chat_rooms.all()).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_rooms"
    )
    # joined_at: 사용자가 채팅방에 참여한 시간 (자동으로 현재 시간 기록).
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름 설정
        db_table = "chat_participants"
        # room과 user 쌍은 유일해야 합니다 (한 사용자가 한 방에 두 번 참여할 수 없음).
        unique_together = ("room", "user")
        # 관리자 페이지 등에서 표시될 단수 이름
        verbose_name = "채팅방 참여자"
        # 관리자 페이지 등에서 표시될 복수 이름
        verbose_name_plural = "채팅방 참여자들"


# ChatMessage 모델: 채팅방 내에서 주고받는 개별 메시지를 나타냅니다.
# 연동: ChatRoom, User 모델과 ForeignKey 관계로 연동됩니다.
# 기능: 메시지의 내용, 발신자, 발송 시간 등을 저장합니다.
class ChatMessage(models.Model):
    # room: 메시지가 속한 ChatRoom을 참조합니다.
    # CASCADE: 참조하는 ChatRoom이 삭제되면 메시지도 함께 삭제됩니다.
    # related_name='messages': ChatRoom 객체에서 이 방의 메시지들을 역참조할 때 사용합니다 (예: room.messages.all()).
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    # sender: 메시지를 보낸 사용자를 참조합니다.
    # settings.AUTH_USER_MODEL: Django의 현재 활성화된 사용자 모델을 참조합니다 (CustomUser).
    # CASCADE: 참조하는 User가 삭제되면 메시지도 함께 삭제됩니다.
    # related_name='sent_messages': User 객체에서 이 사용자가 보낸 메시지들을 역참조할 때 사용합니다 (예: user.sent_messages.all()).
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    # content: 메시지 내용. ERD에 따라 VARCHAR(2083)으로 설정.
    content = models.CharField(max_length=2083)
    # sent_at: 메시지 발송 시간 (자동으로 현재 시간 기록).
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 데이터베이스 테이블 이름 설정
        db_table = "chat_messages"
        # 메시지를 가져올 때 sent_at 필드를 기준으로 내림차순 정렬합니다 (최신 메시지가 먼저 오도록).
        ordering = ["-sent_at"]
        # 관리자 페이지 등에서 표시될 단수 이름
        verbose_name = "채팅 메시지"
        # 관리자 페이지 등에서 표시될 복수 이름
        verbose_name_plural = "채팅 메시지들"
