from asgiref.sync import async_to_sync

from chat.models import Message
from common.consumers.base import JWTAuthenticatedConsumer
from config import settings
from chat.serializers import MessageSerializer, MessageCreateSerializer

User = settings.AUTH_USER_MODEL


class ChatConsumer(JWTAuthenticatedConsumer):
    chat_type = 'chat_message'

    def prepare_connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        return

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

    def chat_message(self, event):
        # obj = Message.objects.get(id=event['message'])
        # message = MessageSerializer(instance=obj).data
        self.send_json(event['message'])

    def create_message(self, event):
        event['conversation'] = self.room_name
        event['sender'] = self.user.pk

        serializer = MessageCreateSerializer(data=event)
        serializer.is_valid()
        return serializer.save()

