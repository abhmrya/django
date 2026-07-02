from .models import Room
from channels.db  import database_sync_to_async

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

    room.participants.add(user1, user2)

    return room

from channels.db import database_sync_to_async
from .models import Message


@database_sync_to_async
def save_message(room, sender, content):

    return Message.objects.create(
        room=room,
        sender=sender,
        content=content
    )