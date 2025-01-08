from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import UserTagForm
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def logout_view(request):

    logout(request)  # Logs out the user
    
    return redirect('login')

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
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def profile_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'users/profile_details.html', {'user': user})

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserTagForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a profile or another page
    else:
        form = UserTagForm(instance=user)
    return render(request, 'users/update_profile.html', {'form': form})