# from django.shortcuts import render

# # Create your views here.
# def login_page(request):
#     return render(request, "login.html")

# def home(request):
#     return render(request, "home.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_page(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/home/")

    return render(request, "login.html")

def home(request):
    return render(request, "home.html")
