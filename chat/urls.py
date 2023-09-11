from django.urls import path
from django.contrib.auth import views
from .views import chat


urlpatterns = [
    path('chat/' , chat , name='chat'),
   
]