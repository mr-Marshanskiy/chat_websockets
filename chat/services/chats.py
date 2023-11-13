import datetime

from chat.factories.chats import UserChatFactory,  MessageFactory
from chat.serializers.chats import MessageSerializer, MessageCreateSerializer


class UserChatService:
    factory = UserChatFactory

    def update_last_seen(self, user_id, chat_id):
        factory = self.factory()
        data = {'last_seen': datetime.datetime.now()}
        obj = factory.get_user_chat(user_id, chat_id)
        if not obj:
            return
        self.factory().update_user_chat(obj, data)
        return


class MessageService:
    factory = MessageFactory

    def get_last_messages(self, chat_id):
        queryset = self.factory().get_chat_messages(chat_id)
        serializer = MessageSerializer(queryset, many=True).data
        return serializer

    def create_websocket_message(self, data):
        serializer = MessageCreateSerializer(data=data)
        serializer.is_valid()
        return serializer.save()

    def get_message_data(self, obj):
        return MessageSerializer(instance=obj).data

    def get_user_for_chat_update_due_message(self, message):
        user_ids = set(self.factory().get_user_ids_from_message(message))
        return user_ids

    def get_user_for_notification_due_message(self, message):
        user_ids = set(self.factory().get_user_ids_from_message(message))
        user_ids.remove(message.sender.pk)
        return user_ids
