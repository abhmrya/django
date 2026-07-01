from django.urls import path
from .consumers import PrivateConsumer

websocket_urlpatterns = [
    path("ws/private/<str:username>/", PrivateConsumer.as_asgi()),
]