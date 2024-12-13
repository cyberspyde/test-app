import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Testing.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from Testing.middleware import JWTAuthMiddleware
from api.routing import websocket_urlpatterns
from channels.layers import get_channel_layer
from channels.auth import AuthMiddlewareStack
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

channel_layer = get_channel_layer()