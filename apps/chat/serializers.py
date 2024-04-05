from rest_framework import serializers
from apps.chat.models import Thread, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ThreadMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'is_read']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'thread', 'sender', 'text', 'is_read']


class ThreadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = ThreadMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'messages']
