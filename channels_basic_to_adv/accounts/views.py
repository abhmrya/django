from django.shortcuts import render, redirect
from .forms import RegisterForm


def home(request):
    return render(request, "accounts/home.html")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        print("Is Valid :", form.is_valid())
        print("Errors :", form.errors)

        if form.is_valid():
            form.save()
            print("User Saved Successfully")
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    return render(request, "accounts/login.html")


def logout_view(request):
    return redirect("home")