from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# User Registration form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
        # add id and placeholder to the input field
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'enter your full name'}),
            'username': forms.TextInput(attrs={'placeholder': 'enter your username'}),
            'email': forms.TextInput(attrs={'placeholder': 'enter your email'})
        }
    # add class to the input field
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class': 'form-control form-control-lg'})

# User Profile form
class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
    # add class to the input field
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs.update({'class': 'form-control form-control-lg'})