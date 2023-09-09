from django.urls import path

from . import consumers

websocket_urlpatterns = [
        path("ws/performances/<int:performance_id>",
             consumers.ChatConsumer.as_asgi()),
]
