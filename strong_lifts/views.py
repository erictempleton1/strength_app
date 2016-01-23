from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from forms import RegisterForm


def index(request):
    return render(request, 'strong_lifts/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #form.save()
            return HttpResponseRedirect('/stronglifts')
    else:
        form = RegisterForm()
    return render(request, 'strong_lifts/register.html', {'form': form})

def login_user(request):
    username = request.post['username']
    password = request.post['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            pass
            # return inactive user message here
    else:
        pass
        # return invalid login message
    return render(request, 'strong_lifts/login.html')

def logout_user(request):
    logout(request)
    # todo - add redirect here