import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add to group
        await self.channel_layer.group_add("new_dialogue", self.channel_name)

        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from group
        await self.channel_layer.group_discard("new_dialogue", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        # Send message to group
        await self.channel_layer.group_send(
            "new_dialogue",
            {
                "type": "dialogue.message",
                "dialogue": "test",
            }
        )

    async def dialogue_message(self, event):
        #@REVISIT
        # dialogue = event["dialogue"]
        await self.send(text_data=json.dumps({"dialogue": "temporary"}))
