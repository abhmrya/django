from django.urls import path
from . import views

urlpatterns = [
    path("channel_layer_app", views.home, name="channel_home"),
]