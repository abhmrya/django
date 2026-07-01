from django.urls import path
from .consumers import PrivateChatConsumer

websocket_urlpatterns = [
    path("ws/private-chat/", PrivateChatConsumer.as_asgi()),
]