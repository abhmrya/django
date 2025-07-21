from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer
import asyncio
import time  # ✅ Required for SyncConsumer

class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("✅ WebSocket connected (async)")
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("📨 Received from client (async):", text_data)
        for i in range(50):
            await self.send(text_data=str(i))
            await asyncio.sleep(1.4)

    async def disconnect(self, close_code):
        print(f"❌ WebSocket disconnected with code {close_code} (async)")
