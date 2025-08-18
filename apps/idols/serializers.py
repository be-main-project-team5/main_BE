from rest_framework import serializers

from .models import Idol


class IdolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idol
        fields = "__all__"


class IdolGroupSerializer(serializers.ModelSerializer):
    """아이돌의 그룹 정보만 수정하기 위한 시리얼라이저"""
    class Meta:
        model = Idol
        fields = ['group']



