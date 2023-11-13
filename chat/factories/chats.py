from chat.factories.queries.chats import UserChatQueriesFactory
from chat.models import UserChat, Message
from common.factories.base import BaseFactory


class UserChatFactory(BaseFactory):
    model = UserChat
    queries = UserChatQueriesFactory

    def get_user_chats(self, user_id):
        return self.model.objects.filter(
            user_id=user_id,
        ).annotate(
            unread_messages=self.queries.unread_messages(),
            # last_message_time=self.queries.last_message_time(),
        )

    def get_user_chat(self, user_id, chat_id):
        return self.model.objects.filter(user_id=user_id, chat_id=chat_id).first()

    def update_user_chat(self, obj, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()


class MessageFactory(BaseFactory):
    model = Message
    queries_factory = None

    def get_message(self, message_id):
        return self.model.objects.filter(id=message_id).first()

    def get_chat_messages(self, chat_id):
        return self.model.objects.filter(chat_id=chat_id).order_by('-timestamp')

    def get_user_ids_from_message(self, message):
        return message.chat.users.values_list('user_id', flat=True)
