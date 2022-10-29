from django.urls import path
from . import consumers

websocket_paths = [
    path('ws/chat/<groupname>/', consumers.ChatConsumer),
    path('ws/personal/chat/<otheruser>/', consumers.PersonalChatConsumer),
]