from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "username", "name": "email", "type": "text"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "password", "name": "password", "type": "password",
               "value": ""}))


class LogoutForm(forms.Form):
    pass
