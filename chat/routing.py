from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chatroom/<chatroom_name>', consumers.ChatRoomConsumer.as_asgi()),
]
