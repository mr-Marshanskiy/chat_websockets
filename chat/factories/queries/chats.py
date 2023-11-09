from django.db.models import *
from django.db.models.functions import *

from chat.models import Message


class UserChatQueriesFactory:

    @staticmethod
    def unread_messages():
        return Count(
            'chat__messages', distinct=True,
            filter=Q(chat__messages__timestamp__gt=F('last_seen'))
        )
