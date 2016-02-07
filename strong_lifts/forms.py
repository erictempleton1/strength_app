import datetime

from django import forms
from models import StrongLifts
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)


class StrongLiftsForm(forms.ModelForm):
    ex_options = [
        ('Squat', 'Squat'),
        ('Bench Press', 'Bench Press'),
        ('Row', 'Row'),
        ('Deadlift', 'Deadlift'),
        ('OH Press', 'OH Press')
    ]

    added_at = forms.DateField(required=True, widget=SelectDateWidget(), initial=datetime.date.today)
    exercise_weight = forms.IntegerField(required=True)
    exercise_reps = forms.IntegerField(required=True)
    exercise_sets = forms.IntegerField(required=True)
    exercise_name = forms.ChoiceField(required=True, widget=forms.Select, choices=ex_options)

    class Meta:
        model = StrongLifts
        fields = ('added_at', 'exercise_name', 'exercise_weight', 'exercise_sets', 'exercise_reps')