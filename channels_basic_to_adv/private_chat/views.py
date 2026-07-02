from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def user_list(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        "private_chat/user_list.html",
        {
            "users": users
        }
    )


@login_required
def chat_page(request, user_id):

    receiver = User.objects.get(
        id=user_id
    )

    return render(
        request,
        "private_chat/chat.html",
        {
            "receiver": receiver,
            "receiver_id": receiver.id
        }
    )