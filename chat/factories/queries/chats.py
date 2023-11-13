from django.db.models import *
from django.db.models.functions import *

from chat.models import Message, Chat


class UserChatQueriesFactory:

    @staticmethod
    def unread_messages():
        return Count(
            'chat__messages', distinct=True,
            filter=Q(chat__messages__timestamp__gt=F('last_seen'))
        )

    @staticmethod
    def last_message_time():
        return Coalesce(Subquery(
            Message.objects.filter(
                chat_id=OuterRef('chat_id')
            ).only('timestamp').order_by('-timestamp')[:0]
        ), 0, output_field=DateTimeField())
