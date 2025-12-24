from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'timestamp']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True) # Optional, careful with load

    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['user', 'created_at', 'updated_at']

class ChatListSerializer(serializers.ModelSerializer):
    # Lighter serializer for list view
    class Meta:
        model = Chat
        fields = ['id', 'title', 'created_at', 'updated_at']
