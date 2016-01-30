from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from models import StrongLifts
from forms import RegisterForm, LoginForm, StrongLiftsForm


def index(request):
    return render(request, 'strong_lifts/index.html')

# todo - add last workout date check and next workout calculation
# todo make form more intuitive
def user_page(request, username):
    # check that user exists
    get_object_or_404(User, username=username)

    # get user activities if they do exist
    get_user_activity = StrongLifts.objects.filter(user__username=username)

    if request.method == 'POST':
        form = StrongLiftsForm(request.POST)
        if form.is_valid():
            # get form data
            exercise_name = form.cleaned_data['exercise_name']
            exercise_sets = form.cleaned_data['exercise_sets']
            exercise_reps = form.cleaned_data['exercise_reps']
            exercise_weight = form.cleaned_data['exercise_weight']

            new_workout = StrongLifts(exercise_name=exercise_name,
                                      exercise_sets=exercise_sets,
                                      exercise_reps=exercise_reps,
                                      exercise_weight=exercise_weight,
                                      user=request.user)
            new_workout.save()
            return HttpResponseRedirect('/stronglifts/u/{0}'.format(request.user.username))
    else:
        form = StrongLiftsForm()
    return render(request, 'strong_lifts/user_page.html',
                  context={
                      'form': form,
                      'get_user_activity': get_user_activity,
                      'username': username
                    }
                  )

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # save new user
            user = form.save()
            user.set_password(user.password)
            user.save()

            # authenticate the new user and log them in
            new_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
            )
            login(request, new_user)
            return HttpResponseRedirect('/stronglifts')
    else:
        form = RegisterForm()
    return render(request, 'strong_lifts/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # get username and pw from post data, and try to authenticate
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/stronglifts')
    else:
        form = LoginForm()
    return render(request, 'strong_lifts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/stronglifts')