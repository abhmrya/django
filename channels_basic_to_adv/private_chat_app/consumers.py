from channels.generic.websocket import AsyncWebsocketConsumer
import json

online_users = {}

class PrivateConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.username = self.scope["url_route"]["kwargs"]["username"]

        online_users[self.username] = self.channel_name

        print(online_users)

        await self.accept()

    async def receive(self, text_data):
        print("Receiver Called")

        data = json.loads(text_data)

        print(data)

        to_user = data['to']
        message = data['message']

        if to_user in online_users:

            await self.channel_layer.send(
                online_users[to_user],{
                    "type":"chat.message",
                    "from": self.username,
                    "message":message
                }
            )
        else:

            await self.send(text_data=json.dumps({
                "from":"Server",
                "message":"User offline"
            }))

    async def chat_message(self, event):
        print("chat_message called")

        print(event)

        await self.send(
            text_data=json.dumps({
                "from":event["from"],
                "message":event["message"]
            })
        )

    async def disconnect(self, close_code):
        print(f'{self.username} Disconnected')

        if self.username in online_users:
            del online_users[self.username]
        
        print(online_users)