from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws/code_editor/<str:room_id>/', consumers.CodeEditorConsumer.as_asgi()),
]