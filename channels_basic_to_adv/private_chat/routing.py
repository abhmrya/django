from django.urls import re_path

from .consumers import (
    PrivateChatConsumer,
    UserStatusConsumer,
)

websocket_urlpatterns = [

    re_path(
        r"ws/private-chat/(?P<user_id>\d+)/$",
        PrivateChatConsumer.as_asgi(),
    ),

    re_path(
        r"ws/users/$",
        UserStatusConsumer.as_asgi(),
    ),

]