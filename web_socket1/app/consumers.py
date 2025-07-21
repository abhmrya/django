from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocket connected....', event)
        print("channel Layer...", self.channel_layer)
        print("channel name...", self.channel_name)

        # Add this channel to the "programmers" group
        await self.channel_layer.group_add(
            'programmers',
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('websocket received from client....', event)

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            'programmers',
            {
                'type': 'chat.message',
                'message': event['text'],
            }
        )

    async def chat_message(self, event):
        # Send the message back to WebSocket client
        await self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })

    async def websocket_disconnect(self, event):
        print('websocket disconnected....', event)

        # Remove this channel from the group
        await self.channel_layer.group_discard(
            'programmers',
            self.channel_name
        )

        raise StopConsumer()
