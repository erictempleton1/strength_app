import datetime

from django import forms
from models import StrongLifts
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class StrongLiftsForm(forms.ModelForm):
    ex_options = [
        ('Squat', 'Squat'),
        ('Bench Press', 'Bench Press'),
        ('Row', 'Row'),
        ('Deadlift', 'Deadlift'),
        ('OH Press', 'OH Press')
    ]

    added_date = forms.DateField(input_formats=['%m/%d/%Y'], initial=datetime.datetime.today)
    exercise_weight = forms.IntegerField(required=True)
    exercise_reps = forms.IntegerField(required=True)
    exercise_sets = forms.IntegerField(required=True)
    exercise_name = forms.ChoiceField(widget=forms.Select,
                                              required=True,
                                              choices=ex_options)

    class Meta:
        model = StrongLifts
        fields = ('added_date', 'exercise_name', 'exercise_weight', 'exercise_sets', 'exercise_reps')