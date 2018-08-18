from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from messenger.consumers import MessagerConsumer
#f#rom bootcamp.notifications.consumers import NotificationsConsumer
# from bootcamp.notifications.routing import notifications_urlpatterns
# from bootcamp.messager.routing import messager_urlpatterns

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
 #               url(r'^notifications/$', NotificationsConsumer),
                url(r'^(?P<username>[^/]+)/$', MessagerConsumer),
            ])
        ),
    ),
})