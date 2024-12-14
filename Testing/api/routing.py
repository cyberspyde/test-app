# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from Testing.middleware import JWTAuthMiddlewareStack
from api.consumers import TestRoomConsumer
from django.urls import re_path
from .consumers import TestRoomConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter([
            re_path(r"ws/test/(?P<room_key>\w+)/$", TestRoomConsumer.as_asgi()),
        ])
    ),
})