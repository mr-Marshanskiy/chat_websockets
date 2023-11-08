from crum import get_current_user
from django.db.models import Q

from chat.models import Message, Conversation
from users.serializers import UserSerializer
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    is_message_mine = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ('conversation',)

    def get_is_message_mine(self, instance):
        if instance.sender == get_current_user():
            return True
        return False


class MessageCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)
    attachment = serializers.FileField(
        write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Message
        fields = ('conversation', 'sender', 'message', 'attachment',)

    def validate(self, attrs):
        attrs['text'] = attrs.pop('message')
        return attrs


class ConversationListSerializer(serializers.ModelSerializer):
    initiator = UserSerializer()
    receiver = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('id', 'initiator', 'receiver', 'last_message')

    def get_last_message(self, instance):
        message = instance.messages.first()
        return MessageSerializer(instance=message).data


class ConversationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ('id', 'receiver',)

    def validate(self, attrs):
        attrs['initiator'] = get_current_user()
        return attrs

    def create(self, validated_data):
        initiator = validated_data.pop('initiator', None)
        receiver = validated_data.pop('receiver', None)

        instance = Conversation.objects.filter(
            Q(initiator=initiator, receiver=receiver) |
            Q(initiator=receiver, receiver=initiator)
        ).first()
        if instance:
            return instance
        instance, created = Conversation.objects.get_or_create(
            initiator=initiator, receiver=receiver
        )
        return instance
