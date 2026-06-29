from django.urls import path
from .consumers import JsonConsumer

websocket_urlpatterns = [
    path("ws/json/", JsonConsumer.as_asgi()),
]