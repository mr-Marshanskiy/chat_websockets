from crum import get_current_user
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema

from common.views import LCRViewSet, ListViewSet
from .models import Conversation, Message

from chat import serializers
from django.db.models import Q

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary='List chats', tags=['Chats']),
    retrieve=extend_schema(summary='Retrieve chats', tags=['Chats']),
    create=extend_schema(summary='Create chats', tags=['Chats']),
)
class ChatView(LCRViewSet):
    queryset = Conversation.objects.all()
    serializer_class = serializers.ConversationListSerializer

    def get_queryset(self):
        user = get_current_user()
        return Conversation.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ConversationCreateSerializer
        return serializers.ConversationListSerializer


@extend_schema_view(
    list=extend_schema(summary='List messages', tags=['Chats']),
)
class MessageView(ListViewSet):
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        chat_id = self.request.parser_context['kwargs'].get('pk')
        return Message.objects.filter(
            conversation_id=chat_id
        ).order_by('timestamp')

