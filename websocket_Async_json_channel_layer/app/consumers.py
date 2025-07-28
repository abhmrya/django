# topic - generic consumer - jsonwebsocketconsumers and asyncjsonwebsocketconsumers


from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from time import sleep
class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print('websocket connected...')
        print('Channel Layer',self.channel_layer)
        print('chanel Name',self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("group Name:",self.group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()      
        # to accept the connection   
        #this handler is called when data received from client
        #with decode JSON content

    def receive_json(self, content, **kwargs):
        print('Message receive from client...',content)
        print('type of message receive from client...',type(content))
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'chat.message',
                'message':content['msg']
            }
        )
    
    def chat_message(self,event):
        print("event...",event)
        self.send_json({
            'message':event['message']
        })


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
