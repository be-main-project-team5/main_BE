from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.groups.serializers import GroupMemberSerializer # GroupMemberSerializer 임포트

from .models import ChatMessage, ChatParticipant, ChatRoom

# Django의 현재 활성화된 사용자 모델을 가져옵니다 (CustomUser).
User = get_user_model()


# ChatMessageSerializer: 채팅 메시지 정보를 직렬화합니다.
# 연동: ChatRoomSerializer에서 중첩하여 사용됩니다.
# 기능: 메시지의 내용, 발신자, 발송 시간 등을 API 응답으로 제공합니다.
class ChatMessageSerializer(serializers.ModelSerializer):
    # sender: 메시지 발신자 정보를 UserSerializer를 통해 읽기 전용으로 중첩하여 보여줍니다.
    # UserSerializer는 제거되었으므로, 필요하다면 GroupMemberSerializer를 사용하거나 별도 정의 필요
    sender = GroupMemberSerializer(read_only=True) # GroupMemberSerializer 사용

    class Meta:
        model = ChatMessage
        # 직렬화할 필드들을 명시합니다。
        fields = ["id", "sender", "content", "sent_at"]


# ChatRoomSerializer: 채팅방 정보를 직렬화합니다.
# 연동: ChatRoomViewSet에서 API 응답을 생성할 때 사용됩니다.
# 기능: 채팅방의 기본 정보와 마지막 메시지, 참여자 목록을 제공합니다.
class ChatRoomSerializer(serializers.ModelSerializer):
    # last_message: ChatRoom 모델의 last_message 필드를 ChatMessageSerializer를 통해 읽기 전용으로 중첩하여 보여줍니다.
    last_message = ChatMessageSerializer(read_only=True)
    # participants: 채팅방 참여자 목록을 SerializerMethodField를 통해 커스텀하여 보여줍니다。
    # ChatParticipant 객체 대신 User 객체 목록을 반환합니다.
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        # 직렬화할 필드들을 명시합니다.
        fields = ["id", "room_name", "last_message", "participants", "created_at"]

    # get_participants 메서드: participants 필드의 값을 계산합니다.
    # obj: 현재 직렬화 중인 ChatRoom 인스턴스입니다.
    def get_participants(self, obj):
        # 해당 채팅방의 모든 ChatParticipant 객체를 가져옵니다.
        participants = obj.participants.all()
        # 각 ChatParticipant 객체에서 user 필드(CustomUser 인스턴스)만 추출하여 리스트를 만듭니다.
        users = [p.user for p in participants]
        # 추출된 User 객체 리스트를 GroupMemberSerializer를 사용하여 직렬화하고, 그 데이터를 반환합니다.
        # many=True: 여러 개의 객체를 직렬화할 때 사용합니다.
        return GroupMemberSerializer(users, many=True).data


# ChatParticipantSerializer: 채팅방 참여자 정보를 직렬화합니다.
# 연동: ChatRoomViewSet의 join/leave 액션 등에서 사용될 수 있습니다.
# 기능: ChatParticipant 모델의 모든 필드를 API 응답으로 제공합니다.
class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        # 모델의 모든 필드를 직렬화합니다.
        fields = "__all__"