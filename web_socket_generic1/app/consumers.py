# app/consumers.py
# topic - generic consumer - websocketconsumers and asyncwebsocketconsumers
# real- time data example 
# real - time data example with front end
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from time import sleep
import asyncio

class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('websocket Connected.....')
        self.accept()  #accept the connection

    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from client....',text_data)
        for i in range(20):
            self.send(text_data=str(i))    # to send data to client
            sleep(1)
        # self.send(bytes_data=data)         #to send binary frame to
    
    def disconnect(self, code):
        print('Websocket Disconnected...',code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('websocket Connected.....')
        await self.accept()  #accept the connection

    async def receive(self, text_data=None, bytes_data=None):
        print('Message Received from client....',text_data)
        for i in range(20):
            await self.send(text_data=str(i))    # to send data to client
            await asyncio.sleep(1)

    async def disconnect(self, code):
        print('Websocket Disconnected...',code)
