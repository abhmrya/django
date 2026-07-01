from django.urls import path
from .consumers import AuthConsumer

websocket_urlpatterns = [
    path("ws/auth/", AuthConsumer.as_asgi()),
]