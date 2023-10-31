from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm

def index(request):
    return render(request, "index.html")



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            user = form.save()
            # import pdb; pdb.set_trace()
            messages.success(request, f'Your account has been created. You can log in now!')
            login(request, user)
            return redirect('index')  # Redirect to the dashboard or any other desired page
    else:
        form = SignUpForm()
    return render(request, 'register/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = SignUpForm(request, request.POST)
        # import pdb; pdb.set_trace()

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the dashboard or any other desired page
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})
