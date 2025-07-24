# app/consumers.py
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json

class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('websocket Connected.....')
        self.accept()  #accept the connection
        # self.close()   #to reject to connection

    def receive(self, text_data=None, bytes_data=None):
        print('Message Received from client....',text_data)
        self.send(text_data="Message from server to client")

        # self.send(bytes_data=data)         #to send binary frame to
        # self.close()                       #force fully disconnect
        self.close(code=3231) 
  
    def disconnect(self, code):
        print('Websocket Disconnected...',code)


class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('websocket Connected.....')
        await self.accept()  #accept the connection
        # self.close()   #to reject to connection

    async def receive(self, text_data=None, bytes_data=None):
        print('Message Received from client....',text_data)
        await self.send(text_data="Message from server to client")

        # self.send(bytes_data=data)         #to send binary frame to
        # self.close()                       #force fully disconnect
        # self.close(code=3231) 
  
    async def disconnect(self, code):
        print('Websocket Disconnected...',code)
