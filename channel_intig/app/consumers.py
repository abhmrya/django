from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("✅ WebSocket connected")
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("📨 Received from client:", text_data)
        for i in range(50):
            print(i)
            await self.send(text_data=str(i))
            await asyncio.sleep(1.5)

    async def disconnect(self, close_code):
        print(f"❌ WebSocket disconnected with code {close_code}")
