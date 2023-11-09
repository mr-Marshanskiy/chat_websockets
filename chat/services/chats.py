import datetime

from chat.factories.chats import UserChatFactory


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
