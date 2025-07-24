# app/consumers.py
# topic - generic consumer - websocketconsumers and asyncwebsocketconsumers
# chat app with dynamic group name
#database


from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Group,Chat
from channels.db import database_sync_to_async
class MyWebsocketConsumer(WebsocketConsumer):
    def connect(self):
        print('WebSocket Connected...')
        print('Channel Layer:', self.channel_layer)
        print('Channel Name:', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('Group Name:', self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        print('successfuly connect...')

    def receive(self, text_data=None, bytes_data=None):
        print('Message received from client:', text_data)
        data = json.loads(text_data)   #json to python
        print("data...",data)
        message = data['msg']
        print(message)
        group = Group.objects.get(name=self.group_name)
        if self.scope['user'].is_authenticated:

            chat = Chat(
                content = data['msg'],
                group = group
            )
            chat.save()
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type':'chat.message',
                    'message':message
                }
            )
        else:
            self.send(text_data=json.dumps({
                "msg":"Login Required"
            }))

    def chat_message(self,event):
        print("event...",event)
        #dumps  python to string
        self.send(text_data=json.dumps({
            'msg':event['message']
        }))

    def disconnect(self, close_code):
        print('WebSocket Disconnected...', close_code)
        print('Channel Layer:', self.channel_layer)
        print('Channel Name:', self.channel_name)
         

class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('websocket Connected.....')
        print('Channel Layer:', self.channel_layer)
        print('Channel Name:', self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print('Group Name:', self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print('successfuly connect...')

    async def receive(self, text_data=None, bytes_data=None):
        print('Message Received from client....',text_data)
        data = json.loads(text_data)   #json to python
        print("data...",data)
        message = data['msg']
        print(message)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        chat = Chat(
            content = data['msg'],
            group = group
        )
        await database_sync_to_async(chat.save())
        await self.channel_layer.group_send(
            await self.group_name,
            { 
                'type':'chat.message',
                'message':message
            }
        )
    async def chat_message(self,event):
        print("event...",event)
        #dumps  python to string
        await self.send(text_data=json.dumps({
            'msg':event['message']
        }))

    async def disconnect(self, code):
        print('Websocket Disconnected...',code)
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )