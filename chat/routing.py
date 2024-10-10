# chat/routing.py
from django.urls import re_path

from . import consumers, consumers_bk, consumers_cp

websocket_urlpatterns = [
    re_path(r"ws/chats/", consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chattest/(?P<userid>[0-9a-fA-F-]+)/$', consumers_cp.ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
