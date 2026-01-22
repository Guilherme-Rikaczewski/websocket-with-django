from django.urls import re_path
from .consumers import AuthenticatedEchoConsumer

websocket_urlpatterns = [
    re_path(r'^ws/secure/$', AuthenticatedEchoConsumer.as_asgi())
]
