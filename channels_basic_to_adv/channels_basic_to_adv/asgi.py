from django.core.asgi import get_asgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channels_basic_to_adv.settings")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from jsonstringify.routing import websocket_urlpatterns as json_routes
from channel_layer_app.routing import websocket_urlpatterns as channel_routes
from group_chat_app.routing import websocket_urlpatterns as group_routes
from private_chat_app.routing import websocket_urlpatterns as private_routes
from auth_chat_app.routing import websocket_urlpatterns as auth_routes
from private_chat.routing import websocket_urlpatterns as private_chat_routes

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                    json_routes +
                    channel_routes +
                    group_routes +
                    private_routes +
                    auth_routes +
                    private_chat_routes
            )
        )
    ),
})