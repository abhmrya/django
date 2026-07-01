from django.shortcuts import render

def chat_page(request):

    return render(
        request,
        "private_chat/chat.html"
    )