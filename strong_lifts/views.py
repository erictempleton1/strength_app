from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'strong_lifts/index.html')

def register(request):
    return render(request, 'strong_lifts/register.html')

def login_user(request):
    return render(request, 'strong_lifts/login.html')

def logout_user(request):
    logout(request)
    # todo - add redirect here