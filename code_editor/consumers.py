from channels.generic.websocket import WebsocketConsumer
import json

class CodeEditorConsumer(WebsocketConsumer):
  def connect(self):
    print(self)
    self.accept()
  
  def disconnect(self, code):
    pass

  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message = text_data_json["message"]

    self.send(text_data=json.dumps({"message": message}))