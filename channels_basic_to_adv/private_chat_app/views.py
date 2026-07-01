from django.shortcuts import render

# Create your views here.
def private_chat(request):
    return render(request,"private_chat.html")