from django.shortcuts import render


def index(request):
    return render(request, 'strong_lifts/index.html')

def register(request):
    return render(request, 'strong_lifts/register.html')

def login(request):
    return render(request, 'strong_lifts/login.html')