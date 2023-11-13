from asgiref.sync import async_to_sync

from chat.factories.chats import UserChatFactory, MessageFactory
from chat.models import Chat, Message
from chat.serializers.chats import ChatListSerializer, MessageCreateSerializer, \
    MessageSerializer, NotificationMessageSerializer
from chat.services.chats import UserChatService, MessageService
from common.consumers.base import JWTAuthenticatedConsumer
from config import settings
from users.services.active_users import ActiveUsersTempSetService

User = settings.AUTH_USER_MODEL


ACTIVE_USERS = set()
active_users_service = ActiveUsersTempSetService(active_users=ACTIVE_USERS)


class MeChatsConsumer(JWTAuthenticatedConsumer):
    chat_type = 'get_chats'
    factory = UserChatFactory
    serializer = ChatListSerializer

    def connect_validation(self):
        super().connect_validation()
        self.room_group_name = f"chats_user_{self.user.pk}"
        return

    def after_connect(self):
        active_users_service.add_active_user(self.user.pk)
        event = {'type': self.chat_type}
        self.get_chats(event)
        return

    def get_chats(self, event):
        chat_qs = self.factory().get_user_chats(user_id=self.user.pk)
        data = self.serializer(chat_qs, many=True).data
        self.send_json(data)

    def disconnect(self, close_code):
        active_users_service.rm_active_user(self.user.pk)
        super().disconnect(close_code)


class MeChatNotificationsConsumer(JWTAuthenticatedConsumer):
    chat_type = 'get_chat_notifications'
    factory = MessageFactory
    serializer = NotificationMessageSerializer

    def connect_validation(self):
        super().connect_validation()
        self.room_group_name = f"chat_notification_user_{self.user.pk}"
        return

    def get_chat_notifications(self, event):
        message_id = event.get('message')
        message = self.factory().get_message(message_id)
        data = self.serializer(message).data
        self.send_json(data)

    def disconnect(self, close_code):
        active_users_service.rm_active_user(self.user.pk)
        super().disconnect(close_code)


class ChatConsumer(JWTAuthenticatedConsumer):
    chat_type = 'chat_message'
    user_chat_service = UserChatService
    message_service = MessageService

    def prepare_connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        return

    def after_connect(self):
        self.user_chat_service().update_last_seen(
            user_id=self.user.pk, chat_id=self.room_name
        )
        messages = self.message_service().get_last_messages(chat_id=self.room_name)
        self.send_json(messages)
        self._refresh_user_chats()

    def receive_json(self, text_data=None, **kwargs):
        message = self._create_message(text_data)
        self._send_message(message)
        self.user_chat_service().update_last_seen(
            user_id=self.user.pk, chat_id=self.room_name
        )
        self._update_user_chats(message)
        self._send_user_notifications(message)

        return

    def chat_message(self, event):
        self.send_json(event.get('message'))

    def _create_message(self, data):
        data['chat'] = self.room_name
        data['sender'] = self.user.pk
        return self.message_service().create_websocket_message(data)

    def _send_message(self, message):
        event = {
            'type': self.chat_type,
            'message': self.message_service().get_message_data(message)
        }
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, event,
        )
        return

    def _update_user_chats(self, message):
        event = {'type': 'get_chats'}

        chat_users = self.message_service().get_user_for_chat_update_due_message(message)
        target_users = active_users_service.select_only_active(chat_users)

        for user_id in target_users:
            async_to_sync(self.channel_layer.group_send)(
                f'chats_user_{user_id}', event
            )
        return

    def _send_user_notifications(self, message):
        event = {
            'type': 'get_chat_notifications',
            'message': message.pk,
        }

        chat_users = self.message_service().get_user_for_notification_due_message(message)
        target_users = active_users_service.select_only_active(chat_users)

        for user_id in target_users:
            async_to_sync(self.channel_layer.group_send)(
                f'chat_notification_user_{user_id}', event
            )
        return

    def _refresh_user_chats(self):
        event = {'type': 'get_chats'}

        async_to_sync(self.channel_layer.group_send)(
            f'chats_user_{self.user.pk}', event,
        )
        return
