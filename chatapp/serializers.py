from rest_framework import serializers
from .models import Conversation

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.CharField()

class ResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    session_id = serializers.CharField()