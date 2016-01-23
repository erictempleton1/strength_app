from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from forms import RegisterForm, LoginForm


def index(request):
    return render(request, 'strong_lifts/index.html')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            #login(request, user)
            return HttpResponseRedirect('/stronglifts')
    else:
        form = RegisterForm()
    return render(request, 'strong_lifts/register.html', {'form': form})

# todo - add login template
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # get username and pw from post data, and try to authenticate
        username = request.post['username']
        password = request.post['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/stronglifts')
            else:
                pass
                # return inactive user message here
        else:
            pass
            # return invalid login message
        return render(request, 'strong_lifts/login.html', {'form': form})
    return render(request, 'strong_lifts/login.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/stronglifts')