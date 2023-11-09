from crum import get_current_user
from django.db.models import Q

from chat.models import Message, Chat
from users.serializers import UserSerializer
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    is_message_mine = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ('chat',)

    def get_is_message_mine(self, instance):
        if instance.sender == get_current_user():
            return True
        return False


class MessageCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Message
        fields = ('chat', 'sender', 'message',)

    def validate(self, attrs):
        attrs['text'] = attrs.pop('message')
        return attrs


class ChatListSerializer(serializers.ModelSerializer):
    chat_id = serializers.CharField()
    unread_messages = serializers.IntegerField()
    name = serializers.CharField(source='chat.name')

    class Meta:
        model = Chat
        fields = ('chat_id', 'name', 'unread_messages')


class NotificationMessageSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField(source='chat.id')
    name = serializers.CharField(source='chat.name')
    sender = serializers.CharField(source='sender.full_name')

    class Meta:
        model = Message
        fields = ('chat_id', 'name', 'text', 'sender', 'timestamp')



# class ConversationCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Conversation
#         fields = ('id', 'receiver',)
#
#     def validate(self, attrs):
#         attrs['initiator'] = get_current_user()
#         return attrs

    # def create(self, validated_data):
    #     initiator = validated_data.pop('initiator', None)
    #     receiver = validated_data.pop('receiver', None)
    #
    #     instance = Conversation.objects.filter(
    #         Q(initiator=initiator, receiver=receiver) |
    #         Q(initiator=receiver, receiver=initiator)
    #     ).first()
    #     if instance:
    #         return instance
    #     instance, created = Conversation.objects.get_or_create(
    #         initiator=initiator, receiver=receiver
    #     )
    #     return instance
