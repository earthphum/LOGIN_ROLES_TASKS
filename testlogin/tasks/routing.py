# tasks/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/tasks/", consumers.TaskConsumer.as_asgi()),
]
