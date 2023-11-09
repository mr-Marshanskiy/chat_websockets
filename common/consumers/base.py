import pdb

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from common.consumers.mixins import JWTConsumerMixin
from common.services.orm_tools import get_user_by_jwt


class WebSocketValidationError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class BaseJsonWebsocketConsumer(JsonWebsocketConsumer):
    room_group_name = None
    chat_type = None

    def get_headers(self):
        headers = dict(self.scope.get('headers'))
        return {
            key.decode('utf-8'): value.decode('utf-8')
            for key, value in headers.items()
        }

    def get_params(self):
        param_str = self.scope.get('query_string').decode('utf-8')
        params_str_list = param_str.split('&')
        params = dict()

        for param in params_str_list:
            key, value = param.split('=')
            params[key] = value
        return params

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive_json(self, text_data=None, **kwargs):
        chat_type = {'type': self.chat_type}
        return_dict = {**chat_type, **text_data}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    def join_to_room_group(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        return

    def connect_validation(self):
        """Any validation before connecting"""
        pass

    def prepare_connect(self):
        """Additional actions before connecting"""
        pass

    def after_connect(self):
        """Additional actions after connecting"""
        pass

    def connect(self):
        try:
            self.prepare_connect()
            self.connect_validation()
            self.join_to_room_group()
            self.accept()
            self.after_connect()
        except ConnectionError as e:
            self.close(4000)


class JWTAuthenticatedConsumer(BaseJsonWebsocketConsumer, JWTConsumerMixin):
    def get_current_user(self):
        user = get_user_by_jwt(self.get_jwt_from_params())
        return user

    def connect_validation(self):
        self.user = self.get_current_user()
        if not self.user:
            raise ConnectionError(4000, 'User not found')

