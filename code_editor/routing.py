from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws/code_editor/<str:room_id>/<str:user_name>/<str:user_id>/', consumers.CodeEditorConsumer.as_asgi()),
]