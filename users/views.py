from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomAuthenticationForm, UserRegistrationForm
from .models import CustomUser, Tag
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth import authenticate, logout, login as auth_login

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
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def profile_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    tags = user.tags.all()
    context = {
        'user': user,
        "user_tags": tags
    }
    return render(request, 'users/profile_details.html', context)

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile' , user_id=user.id)
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'users/update_profile.html', {'form': form,
                                                         "user": user})

@login_required
def add_tags(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    tags = request.POST.get('tags', '')

    if request.method == 'POST':
        if tags:
            user.tags.clear()
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                user.tags.add(tag)
            user.save()

        return redirect('profile', user_id=user.id)
    tags = Tag.objects.all()
    user_tags = user.tags.all()
    tag_list = ",".join([tag.name for tag in user_tags])
    print(tag_list)

    context = {
        "user": user,
        "tags": tags,
        "user_tags": tag_list
    }
    return render(request, 'users/add_tags.html', context)
