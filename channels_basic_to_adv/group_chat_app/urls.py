from django.urls import path
from . import views

urlpatterns = [
    path("group-chat/", views.index),
]