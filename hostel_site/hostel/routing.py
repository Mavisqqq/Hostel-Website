from django.urls import path
from hostel.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),
]
