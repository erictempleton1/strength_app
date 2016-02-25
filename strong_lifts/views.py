from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from models import StrongLifts
from forms import RegisterForm, LoginForm, StrongLiftsForm


def index(request):
    return render(request, 'strong_lifts/index.html')

# todo - add last workout date check and next workout calculation
def user_page(request, username):
    # check that user exists
    get_object_or_404(User, username=username)

    # get user activities if they do exist
    get_user_activity = StrongLifts.objects.filter(user__username=username).order_by('-added_at')

    if request.method == 'POST':
        form = StrongLiftsForm(request.POST)
        if form.is_valid():
            # get form data
            added_at = form.cleaned_data['added_at']
            exercise_name = form.cleaned_data['exercise_name']
            exercise_sets = form.cleaned_data['exercise_sets']
            exercise_reps = form.cleaned_data['exercise_reps']
            exercise_weight = form.cleaned_data['exercise_weight']

            new_workout = StrongLifts(added_at=added_at,
                                      exercise_name=exercise_name,
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
                      'get_user_activity': get_user_activity[0:15],
                      'username': username,
                      'user_maxes': current_maxes(request.user, get_user_activity)
                    }
                  )

# todo - this can probably be reworked to include sets, reps, date ect. and only use one query
# for example - just work with the full query set dict and parse out heaviest info from there
def current_maxes(user_obj, exercise_query):
    """
    Gets the highest weight for each exercise by first getting distinct exercise names,
    then aggregating max on each iteration and adding to empty dict.
    This is pretty inefficient for right now.
    """
    max_weight_obj = {}
    lifts = exercise_query.values()
    return lifts

@login_required(login_url='/stronglifts/login/')
def update_exercise(request, username, exercise_id):

    # get the exercise object and make sure it belongs to the user
    exercise_edit = get_object_or_404(StrongLifts, id=exercise_id, user=request.user)

    if request.method == 'POST':
        form = StrongLiftsForm(request.POST,
                initial={
                    'added_at': exercise_edit.added_at,
                    'exercise_name': exercise_edit.exercise_name,
                    'exercise_weight': exercise_edit.exercise_weight,
                    'exercise_sets': exercise_edit.exercise_sets,
                    'exercise_reps': exercise_edit.exercise_reps
                }
        )
        if form.is_valid():
            exercise_edit.added_at = form.cleaned_data['added_at']
            exercise_edit.exercise_name = form.cleaned_data['exercise_name']
            exercise_edit.exercise_sets = form.cleaned_data['exercise_sets']
            exercise_edit.exercise_reps = form.cleaned_data['exercise_reps']
            exercise_edit.exercise_weight = form.cleaned_data['exercise_weight']
            exercise_edit.save()
            return HttpResponseRedirect('/stronglifts/u/{0}'.format(request.user.username))
    else:
        form = StrongLiftsForm(
                initial={
                    'added_at': exercise_edit.added_at,
                    'exercise_weight': exercise_edit.exercise_weight,
                    'exercise_sets': exercise_edit.exercise_sets,
                    'exercise_reps': exercise_edit.exercise_reps,
                    'exercise_name': exercise_edit.exercise_name
                }
        )
    return render(request, 'strong_lifts/update_exercise.html',
                  context={
                        'form': form,
                        'exercise_edit': exercise_edit,
                        'username': username,
                        'exercise_id': exercise_id
                    }
                  )

@login_required(login_url='/stronglifts/login/')
def remove_exercise(request, username, exercise_id):

    # get the exercise object and make sure it belongs to the user
    exercise_to_delete = get_object_or_404(StrongLifts, id=exercise_id, user=request.user)

    if request.method == 'POST':
        form = StrongLiftsForm(request.POST)
        if form.is_valid():
            exercise_to_delete.delete()
            return HttpResponseRedirect('/stronglifts/u/{0}'.format(request.user.username))
    else:
        form = StrongLiftsForm(
            initial={
                    'added_at': exercise_to_delete.added_at,
                    'exercise_weight': exercise_to_delete.exercise_weight,
                    'exercise_sets': exercise_to_delete.exercise_sets,
                    'exercise_reps': exercise_to_delete.exercise_reps,
                    'exercise_name': exercise_to_delete.exercise_name
                }
        )

        # update form field attrs to be readonly
        # although any changes by the user won't be saved, its a better experience
        form.fields['exercise_weight'].widget.attrs['readonly'] = 'readonly'
        form.fields['exercise_sets'].widget.attrs['readonly'] = 'readonly'
        form.fields['exercise_name'].widget.attrs['readonly'] = 'readonly'
        form.fields['exercise_reps'].widget.attrs['readonly'] = 'readonly'
        form.fields['added_at'].widget.attrs['readonly'] = 'readonly'

        # disable select form dropdowns
        form.fields['exercise_name'].widget.attrs['disabled'] = 'disabled'
        form.fields['added_at'].widget.attrs['disabled'] = 'disabled'

    return render(request, 'strong_lifts/remove_exercise.html',
                  context={
                      'form': form,
                      'exercise_delete': exercise_to_delete,
                      'username': username,
                      'exercise_id': exercise_id
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
                return HttpResponseRedirect('/stronglifts/u/{0}/'.format(username))
    else:
        form = LoginForm()
    return render(request, 'strong_lifts/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/stronglifts/login/')