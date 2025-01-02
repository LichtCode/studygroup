from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import UserTagForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


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