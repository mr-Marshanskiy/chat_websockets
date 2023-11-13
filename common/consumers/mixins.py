from asgiref.sync import async_to_sync


class JWTConsumerMixin:
    def get_jwt_from_headers(self, lookup='authorization',):
        headers = self.get_headers()
        if lookup not in headers:
            return None
        token_name, token_key = headers[lookup].split()
        return token_key

    def get_jwt_from_params(self, lookup='token'):
        params = self.get_params()
        if lookup not in params:
            return None
        return params['token']


class ReceiveDispatch:
    def receive_json(self, text_data=None, **kwargs):
        chat_type = {'type': self.chat_type}
        return_dict = {**chat_type, **text_data}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )
