from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GroupConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.group_name = self.room_name

        print("Room Name :", self.room_name)
        print("Group Name :", self.group_name)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print("Joined :", self.group_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        print("Receive Called")
        print(text_data)

        data = json.loads(text_data)

        # Send message to all users in group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": data["message"]
            }
        )

    async def chat_message(self, event):

        print("chat_message Called")
        print(event)

        await self.send(
            text_data=json.dumps({
                "message": event["message"]
            })
        )

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        print("Left :", self.group_name)