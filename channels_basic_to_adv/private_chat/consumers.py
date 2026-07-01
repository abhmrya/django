from channels.generic.websocket import AsyncWebsocketConsumer


class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print("=" * 50)
        print("WebSocket Connected")
        print("Channel Name :", self.channel_name)
        print("=" * 50)

        await self.accept()

    async def disconnect(self, close_code):

        print("=" * 50)
        print("WebSocket Disconnected")
        print("=" * 50)