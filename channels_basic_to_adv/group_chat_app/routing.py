from django.urls import path
from .consumers import GroupConsumer

websocket_urlpatterns = [
    # path("ws/group/", GroupConsumer.as_asgi()),

    path("ws/chat/<str:room_name>/", GroupConsumer.as_asgi()),
]