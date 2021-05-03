import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat.routing
import channels.asgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.channel_routing
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})

channel_layer = channels.asgi.get_channel_layer()

