import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User
from django.utils import timezone

from .models import Room, Message


# ==========================================================
# DATABASE FUNCTIONS
# ==========================================================

@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)


@database_sync_to_async
def get_or_create_room(user1, user2):

    room = (
        Room.objects
        .filter(participants=user1)
        .filter(participants=user2)
        .first()
    )

    if room:
        return room

    room = Room.objects.create()

    room.participants.add(user1)
    room.participants.add(user2)

    return room


@database_sync_to_async
def user_connected(user):

    status = user.status

    status.connections += 1
    status.is_online = True

    status.save()


@database_sync_to_async
def user_disconnected(user):

    status = user.status

    if status.connections > 0:
        status.connections -= 1

    if status.connections == 0:

        status.is_online = False
        status.last_seen = timezone.now()

    status.save()


@database_sync_to_async
def save_message(room, sender, message):

    return Message.objects.create(

        room=room,

        sender=sender,

        content=message

    )


@database_sync_to_async
def get_chat_history(room):

    messages = (
        Message.objects
        .filter(room=room)
        .select_related("sender")
        .order_by("created_at")
    )

    history = []

    for msg in messages:

        history.append({

            "id": msg.id,

            "sender": msg.sender.username,

            "message": msg.content,

            "time": msg.created_at.strftime("%I:%M %p"),

            "is_read": msg.is_read

        })

    return history


@database_sync_to_async
def mark_messages_as_read(room, current_user):

    (
        Message.objects

        .filter(room=room)

        .exclude(sender=current_user)

        .update(is_read=True)

    )


# ==========================================================
# CONSUMER
# ==========================================================

class PrivateChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.channel_layer.group_send(

                "online_users",

                {

                    "type":"user_status",

                    "username":self.user.username,

                    "online":True

                }

            )

        self.user = self.scope["user"]

        if not self.user.is_authenticated:

            await self.close()

            return

        self.receiver_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.receiver = await get_user(self.receiver_id)

        self.room = await get_or_create_room(

            self.user,

            self.receiver

        )

        self.room_group_name = f"private_chat_{self.room.id}"

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )

        await user_connected(self.user)

        await self.accept()

        history = await get_chat_history(self.room)

        await self.send(

            text_data=json.dumps({

                "type": "history",

                "messages": history

            })

        )

        await mark_messages_as_read(

            self.room,

            self.user

        )

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type": "online_status",

                "username": self.user.username,

                "online": True

            }

        )

        print("=" * 60)
        print("CONNECTED")
        print("User :", self.user.username)
        print("Receiver :", self.receiver.username)
        print("Room :", self.room.id)
        print("=" * 60)


    async def disconnect(self, close_code):

        await user_disconnected(self.user)

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name

        )

        await self.channel_layer.group_send(

            self.room_group_name,

            {

                "type": "online_status",

                "username": self.user.username,

                "online": False

            }

        )

        print("=" * 60)
        print("DISCONNECTED :", self.user.username)
        print("=" * 60)


    async def receive(self, text_data):

        data = json.loads(text_data)

        action = data.get("action")


        # ==========================================
        # SEND MESSAGE
        # ==========================================

        if action == "message":

            message = data.get("message")

            if not message.strip():
                return

            msg = await save_message(

                self.room,

                self.user,

                message

            )

            await self.channel_layer.group_send(

                self.room_group_name,

                {

                    "type": "chat_message",

                    "message_id": msg.id,

                    "sender": self.user.username,

                    "message": msg.content,

                    "time": msg.created_at.strftime("%I:%M %p")

                }

            )


        # ==========================================
        # USER TYPING
        # ==========================================

        elif action == "typing":

            await self.channel_layer.group_send(

                self.room_group_name,

                {

                    "type": "typing_status",

                    "user": self.user.username

                }

            )


        # ==========================================
        # STOP TYPING
        # ==========================================

        elif action == "stop_typing":

            await self.channel_layer.group_send(

                self.room_group_name,

                {

                    "type": "stop_typing_status",

                    "user": self.user.username

                }

            )
        # ==========================================================
    # CHAT MESSAGE
    # ==========================================================

    async def chat_message(self, event):

        await self.send(

            text_data=json.dumps({

                "type": "message",

                "message_id": event["message_id"],

                "sender": event["sender"],

                "message": event["message"],

                "time": event["time"]

            })

        )


    # ==========================================================
    # USER TYPING
    # ==========================================================

    async def typing_status(self, event):

        # Apne aap ko typing mat dikhao

        if event["user"] == self.user.username:
            return

        await self.send(

            text_data=json.dumps({

                "type": "typing",

                "user": event["user"]

            })

        )


    # ==========================================================
    # STOP TYPING
    # ==========================================================

    async def stop_typing_status(self, event):

        if event["user"] == self.user.username:
            return

        await self.send(

            text_data=json.dumps({

                "type": "stop_typing",

                "user": event["user"]

            })

        )


    # ==========================================================
    # ONLINE / OFFLINE
    # ==========================================================

    async def online_status(self, event):

        await self.send(

            text_data=json.dumps({

                "type": "online_status",

                "username": event["username"],

                "online": event["online"]

            })

        )


    # ==========================================================
    # READ RECEIPT
    # ==========================================================

    async def read_receipt(self, event):

        await self.send(

            text_data=json.dumps({

                "type": "read_receipt",

                "message_id": event["message_id"]

            })

        )


    # ==========================================================
    # ERROR
    # ==========================================================

    async def websocket_disconnect(self, message):

        try:

            await self.disconnect(message["code"])

        except Exception as e:

            print("Disconnect Error :", e)


class UserStatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]

        if not self.user.is_authenticated:

            await self.close()

            return

        self.group_name = "online_users"

        await self.channel_layer.group_add(

            self.group_name,

            self.channel_name

        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(

            self.group_name,

            self.channel_name

        )

    async def user_status(self, event):

        await self.send(

            text_data=json.dumps({

                "username": event["username"],

                "online": event["online"]

            })

        )