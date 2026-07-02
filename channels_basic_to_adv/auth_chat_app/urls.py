from django.urls import path
from auth_chat_app import views

urlpatterns = [
    path("chat/login/", views.login_page),
    path("home/", views.home),
]