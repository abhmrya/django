from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MyConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

        print("=" * 60)
        print("Connected")
        print("Channel Name :", self.channel_name)
        print("=" * 60)


    async def receive(self, text_data):

        # print(self.__dict__)
        
        print(type(self.channel_layer))
        print(self.channel_layer)
        print(type(self.channel_name))
        print(self.channel_name)

        print("\nReceive Method Called")

        print("Raw Data :", text_data)

        data = json.loads(text_data)

        print("Python Dictionary :", data)

        if data["type"] == "send":

            print("Sending Event To Channel Layer")

            await self.channel_layer.send(

                self.channel_name,

                {

                    "type": "chat.message",

                    "message": data["message"]

                }

            )


    async def chat_message(self, event):

        print("\nchat_message() Called")

        print(event)

        await self.send(

            text_data=json.dumps({

                "message": event["message"]

            })

        )


    async def disconnect(self, close_code):

        print("Disconnected")