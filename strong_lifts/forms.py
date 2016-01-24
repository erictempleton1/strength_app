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
    exercise_name = forms.CharField(required=True)
    exercise_weight = forms.IntegerField(required=True)
    exercise_reps = forms.IntegerField(required=True)
    exercise_sets = forms.IntegerField(required=True)

    class Meta:
        model = StrongLifts
        fields = ('exercise_name', 'exercise_weight', 'exercise_reps', 'exercise_reps')