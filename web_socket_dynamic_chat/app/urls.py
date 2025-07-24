from django.urls import path
from . import views

urlpatterns = [
    path('group/<str:group_name>',views.index,name='index'),

]
