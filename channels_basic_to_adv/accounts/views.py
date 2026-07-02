from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterForm


def home(request):
    return render(request, "accounts/home.html")


def register_view(request):

    if request.user.is_authenticated:
        return redirect("user_list")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Registration Successful. Please Login."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("user_list")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        print("Username :", username)
        print("Password :", password)
        print("User :", user)

        if user is not None:

            login(request, user)
            print("Login Success")

            return redirect("user_list")

        else:
            print("Login Failed")

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("login")