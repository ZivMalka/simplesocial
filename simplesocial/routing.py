
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from messenger.views import ThreadView
from messenger.consumer import ChatConsumer


application = ProtocolTypeRouter({

    # WebSocket chat handler
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter([
            url(r"^messenger/(?P<username>[\w.@+-]+)/$", ChatConsumer),
        ])
    ),
    ),
    # Using the third-party project frequensgi, which provides an APRS protocol

})