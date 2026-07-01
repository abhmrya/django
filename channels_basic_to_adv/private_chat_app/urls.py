from django.urls import path
from . import views

urlpatterns = [
    path("private-chat/", views.private_chat),
]