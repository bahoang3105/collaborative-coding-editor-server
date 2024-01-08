from channels.generic.websocket import AsyncWebsocketConsumer
import json

from .editor_manager import EditorManager

class CodeEditorConsumer(AsyncWebsocketConsumer):
	room_id: str
	editor_manager = EditorManager()

	async def connect(self):
		self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
		self.room_group_name = "room_%s" % self.room_id

		# Join room group
		await self.channel_layer.group_add(self.room_group_name, self.channel_name)

		await self.accept()

	async def disconnect(self, code):
		# self.editor_manager.remove_user_from_editor(self.user, self.room_id)
		await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
	
	# Receive message from room group
	async def room_message(self, event): 
		text_data = event["text_data"]

		# Send message to WebSocket
		await self.send(text_data=text_data)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		event = text_data_json["event"]
		data = text_data_json["data"]
		match event:
			case 'user-connect':
				self.handle_user_connect(data)
				
		# broadcase event to all channels in the room
		await self.channel_layer.group_send(
			self.room_group_name, {
				"type": "room_message",
				"text_data": json.dumps({"from": self.user, "event": event, "data": data})
			}
		)
	
	def handle_user_connect(self, data):
		self.user = {
			"name": data["username"],
			"id": data["userId"],
		}
		self.editor_manager.add_user_to_editor(self.user, self.room_id)
