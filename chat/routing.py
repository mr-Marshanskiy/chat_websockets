from django.urls import re_path

from chat.consumers import chats

websocket_urlpatterns = [
    re_path(r'ws/me/chats/$', chats.MeChatsConsumer.as_asgi()),
    re_path(r'ws/me/chats/notifications/$', chats.MeChatNotificationsConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chats.ChatConsumer.as_asgi()),
]
