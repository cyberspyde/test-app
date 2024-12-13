from django.urls import path
from .consumers import TestRoomConsumer

websocket_urlpatterns = [
    path('ws/test/<str:room_key>/', TestRoomConsumer.as_asgi()),
]
