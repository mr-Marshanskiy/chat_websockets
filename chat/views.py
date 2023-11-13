from crum import get_current_user
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema

from common.views import LCRViewSet, ListViewSet
from .models import Chat, Message

from chat.serializers import chats as serializers
from django.db.models import Q

User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary='List chats', tags=['Chats']),
    retrieve=extend_schema(summary='Retrieve chats', tags=['Chats']),
)
class ChatView(ListViewSet):
    queryset = Chat.objects.all()
    serializer_class = serializers.UserChatListSerializer

    def get_queryset(self):
        user = get_current_user()
        return Chat.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        )


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
        ).order_by('timestamp')[20:]

