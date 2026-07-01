from django.shortcuts import render


def index(request):
    return render(request, "group_chat.html")