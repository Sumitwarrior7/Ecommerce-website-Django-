from . import models
from django import forms
from django.forms import TextInput, EmailInput, PasswordInput


# First Model form :-
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'First name'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Last name'}),
            'username': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}),
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
        }


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'password']
        widgets = {
            'email': EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}),
            'password': PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'})
        }

















