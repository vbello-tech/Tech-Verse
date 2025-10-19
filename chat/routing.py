from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/dm/(?P<conversation_id>\d+)/$', consumers.DMConsumer.as_asgi()),
]
