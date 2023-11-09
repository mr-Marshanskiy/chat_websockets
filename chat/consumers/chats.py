from asgiref.sync import async_to_sync

from chat.factories.chats import UserChatFactory
from chat.models import Chat, Message
from chat.serializers.chats import ChatListSerializer, MessageCreateSerializer, \
    MessageSerializer
from chat.services.chats import UserChatService
from common.consumers.base import JWTAuthenticatedConsumer
from config import settings

User = settings.AUTH_USER_MODEL


ACTIVE_USERS = set()


class MeChatsConsumer(JWTAuthenticatedConsumer):
    chat_type = 'get_chats'
    factory = UserChatFactory
    serializer = ChatListSerializer

    def connect_validation(self):
        super().connect_validation()
        self.room_group_name = f"chats_user_{self.user.pk}"
        return

    def after_connect(self):
        event = {'type': self.chat_type}
        self.get_chats(event)
        ACTIVE_USERS.add(self.user.pk)
        return

    def get_chats(self, event):
        chat_qs = self.factory().get_user_chats(self.user)
        data = self.serializer(chat_qs, many=True).data
        self.send_json(data)

    def disconnect(self, close_code):
        super().disconnect(close_code)
        try:
            ACTIVE_USERS.remove(self.user.pk)
        except KeyError:
            pass


class ChatConsumer(JWTAuthenticatedConsumer):
    chat_type = 'chat_message'
    user_chat_service = UserChatService

    def prepare_connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        return

    def after_connect(self):
        self.user_chat_service().update_last_seen(
            self.user.pk,
            self.room_name
        )

        chats = Message.objects.filter(chat_id=self.room_name).order_by('timestamp')
        message = MessageSerializer(chats, many=True).data
        self.send_json(message)


    def receive_json(self, text_data=None, **kwargs):
        chat_type = {'type': self.chat_type}
        return_dict = {**chat_type, **text_data}
        obj = self.create_message(return_dict)
        message = MessageSerializer(instance=obj).data
        return_dict['message'] = message
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

        new_chat_type = {'type': 'get_chats'}
        for user_id in ACTIVE_USERS:
            async_to_sync(self.channel_layer.group_send)(
                f'chats_user_{user_id}', new_chat_type
            )

    def chat_message(self, event):
        self.send_json(event['message'])

    def create_message(self, event):
        event['chat'] = self.room_name
        event['sender'] = self.user.pk

        serializer = MessageCreateSerializer(data=event)
        serializer.is_valid()
        return serializer.save()

