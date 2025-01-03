from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import UserTagForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('create_topic')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserTagForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('create_topic')  # Redirect to a profile or another page
    else:
        form = UserTagForm(instance=user)
    return render(request, 'users/update_profile.html', {'form': form})