import json

from channels.generic.websocket import AsyncWebsocketConsumer


class JsonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connected")

        await self.accept()

    async def receive(self, text_data):

        print("Raw JSON String")
        print(text_data)

        data = json.loads(text_data)

        print("Python Dictionary")
        print(data)

        print(data["name"])
        print(data["age"])

        response = {
            "status": "success",
            "message": "JSON Received Successfully",
            "student": data["name"],
            "age": data["age"]
        }

        await self.send(
            text_data=json.dumps(response)
        )

    async def disconnect(self, close_code):
        print("Disconnected")