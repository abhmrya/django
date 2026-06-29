from django.urls import path
from .consumers import MyConsumer

websocket_urlpatterns = [
    path("ws/channel/", MyConsumer.as_asgi()),
]