from django.contrib import admin

from .models import (
    Room,
    Message,
    UserStatus,
)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "get_participants",
        "created_at",
    )

    search_fields = (
        "participants__username",
    )

    def get_participants(self, obj):

        return ", ".join(

            user.username

            for user in obj.participants.all()

        )

    get_participants.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "room",
        "sender",
        "content",
        "is_read",
        "created_at",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "sender__username",
        "content",
    )


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "is_online",
        "connections",
        "last_seen",
    )

    list_filter = (
        "is_online",
    )

    search_fields = (
        "user__username",
    )