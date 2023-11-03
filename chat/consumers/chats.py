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

    def chat_message(self, event):
        message_obj = self.create_message(event)
        message = MessageSerializer(instance=message_obj).data
        self.send_json(message)

    def create_message(self, event):
        event['conversation'] = self.room_name
        event['sender'] = self.user.pk

        serializer = MessageCreateSerializer(data=event)
        serializer.is_valid()
        return serializer.save()

