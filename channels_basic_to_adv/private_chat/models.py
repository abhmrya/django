from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):

    participants = models.ManyToManyField(
        User,
        related_name="chat_rooms"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        users = self.participants.all()

        return " & ".join(
            user.username
            for user in users
        )


class Message(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.sender.username} : {self.content}"


class UserStatus(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="status"
    )

    is_online = models.BooleanField(
        default=False
    )

    last_seen = models.DateTimeField(
        auto_now=True
    )

    connections = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):

        return self.user.username