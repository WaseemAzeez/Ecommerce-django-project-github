from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def chat(request):
    #if not request.user.is_authenticated:
        #return redirect('login-user') 
    form = UserCreationForm()
    return render(request , 'chat/chat.html' , {'form' : form})
        