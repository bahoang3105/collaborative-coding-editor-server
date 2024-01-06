from channels.generic.websocket import WebsocketConsumer
import json

from .editor_manager import EditorManager

class CodeEditorConsumer(WebsocketConsumer):
  room_id: str
  editor_manager = EditorManager()

  def connect(self):
    self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
    self.user = {
      "name": self.scope["url_route"]["kwargs"]["user_name"],
      "id": self.scope["url_route"]["kwargs"]["user_id"],
    }
    self.editor_manager.add_user_to_editor(self.user, self.room_id)
    self.accept()
  
  def disconnect(self, code):
    self.editor_manager.remove_user_from_editor(self.user, self.room_id)

  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    event = text_data_json["event"]
    data = text_data_json["data"]

    self.send(text_data=json.dumps({"event": event, "data": data}))