from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    username = mo