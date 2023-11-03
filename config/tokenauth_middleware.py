import pdb

from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


def get_user_sync(jwt_token):
    try:
        token = AccessToken(jwt_token)
        user = User.objects.get(id=token['user_id'])
        return user
    except Exception as e:
        return None


class TokenAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        scope['user'] = await self._get_user(scope)
        return await self.inner(scope, receive, send)

    async def _get_user(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name != 'Bearer':
                return None
            return await get_user_sync(token_key)


class JWTWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user = self.get_user()
        return

    def get_user(self):
        headers = dict(self.scope.get('headers'))

        if b'authorization' not in headers:
            self.close()
            return

        token_name, token_key = headers[b'authorization'].decode().split()
        if token_name != 'Bearer':
            self.close('Invalid token format')
            return
        user = get_user_sync(token_key)
        if not user:
            self.close('User not found')
            return
        return user
