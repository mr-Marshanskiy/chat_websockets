import datetime

from chat.factories.chats import UserChatFactory,  MessageFactory
from chat.serializers.chats import MessageSerializer, MessageCreateSerializer, \
    UserChatListSerializer, NotificationMessageSerializer


class UserChatService:
    _factory = UserChatFactory

    def __init__(self, *args, **kwargs):
        self.factory = self._factory()

    def get_user_chats(self, user_id):
        qs = self.factory.get_user_chats(user_id)
        return UserChatListSerializer(qs, many=True).data

    def update_last_seen(self, user_id, chat_id):
        obj = self.factory.get_user_chat(user_id, chat_id)
        if not obj:
            return

        data = {'last_seen': datetime.datetime.now()}
        self.factory.update_user_chat(obj, data)
        return


class MessageService:
    _factory = MessageFactory

    def __init__(self, *args, **kwargs):
        self.factory = self._factory()

    def get_last_messages(self, chat_id):
        queryset = self.factory.get_chat_messages(chat_id)
        serializer = MessageSerializer(queryset, many=True).data
        return serializer

    def create_websocket_message(self, data):
        serializer = MessageCreateSerializer(data=data)
        serializer.is_valid()
        return serializer.save()

    def get_message_data(self, obj):
        return MessageSerializer(instance=obj).data

    def get_user_for_chat_update_due_message(self, message):
        user_ids = set(self.factory.get_user_ids_from_message(message))
        return user_ids

    def get_user_for_notification_due_message(self, message):
        user_ids = set(self.factory.get_user_ids_from_message(message))
        user_ids.remove(message.sender.pk)
        return user_ids

    def get_message_for_notification(self, message_id):
        obj = self.factory.get_object(message_id)
        return NotificationMessageSerializer(obj).data
