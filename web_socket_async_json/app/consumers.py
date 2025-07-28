# topic - generic consumer - jsonwebsocketconsumers and asyncjsonwebsocketconsumers


from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from time import sleep
class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print('websocket connected...')
        self.accept()      
        # to accept the connection   
        #this handler is called when data received from client
        #with decode JSON content

    def receive_json(self, content, **kwargs):
        print('Message receive from client...',content)
        print('type of message receive from client...',type(content))
        self.send_json({'message': 'from server to client'})
        for i in range(20):
            self.send_json({'message':str(i**2)})
            sleep(1)

    def disconnect(self, code):
        print('websocket disconnected...')   


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('websocket connected...')
        await self.accept()    # to accept the connection
        
        #this handler is called when data received from client
        #with decode JSON content

    async def receive_json(self, content, **kwargs):
        print('Message receive from client...',content)
        print('type of message receive from client...',type(content))

        await self.send_json({'message': 'from server to client'})

    async def disconnect(self, code):
        print('websocket disconnected...')   
