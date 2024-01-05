from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
  re_path(r'^ws/code_editor/(?P<room_name>\d+)/', consumers.CodeEditorConsumer.as_asgi()),
]