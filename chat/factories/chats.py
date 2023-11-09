from chat.factories.queries.chats import UserChatQueriesFactory
from chat.models import UserChat, Message


class UserChatFactory:
    model = UserChat
    queries_factory = UserChatQueriesFactory

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queries = self.queries_factory()

    def get_user_chats(self, user):
        return self.model.objects.filter(
            user=user,
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


class MessageFactory:
    model = Message
    queries_factory = None

    def get_message(self, message_id):
        return self.model.objects.filter(
            id=message_id
        ).first()
