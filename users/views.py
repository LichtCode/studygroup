from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomAuthenticationForm, UserRegistrationForm
from .models import CustomUser, Tag
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth import authenticate, logout, login as auth_login

def logout_view(request):

    """
    Logs out the user and redirects to the landing page.

    Args:
        request (object): The request object

    Returns:
        object: Redirect to the landing page
    """
    logout(request)  # Logs out the user
    
    return redirect('landing_page')

def register(request):
    """
    This view handles the registration of a new user.

    If the request is a GET, it renders the registration form.
    If the request is a POST, it validates the form and if valid, saves the user and redirects to login.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login(request):
    """
    Handles user login functionality. If the request method is POST, it
    processes the login form, authenticates the user, and redirects them
    to the dashboard upon successful login. If the request method is not
    POST, it displays the login form.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the dashboard if login is successful, or a rendered
        login page with the form.
    """

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
    """
    Shows the profile of a given user, including all tags they have
    
    Args:
        request (HttpRequest): the request object
        user_id (int): the id of the user whose profile is to be shown
    
    Returns:
        HttpResponse: a rendered HTML page with the user's profile
    """
    user = get_object_or_404(CustomUser, id=user_id)
    tags = user.tags.all()
    context = {
        'user': user,
        "user_tags": tags
    }
    return render(request, 'users/profile_details.html', context)

@login_required
def update_profile(request):
    """
    Updates the profile of the currently logged-in user.

    Handles both GET and POST requests. On GET requests, it displays a form
    pre-filled with the user's current profile information. On POST requests,
    it processes the form submission to update the user's profile with the
    provided data if the form is valid.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the user's profile page if the profile
        update is successful, otherwise renders the profile update page with 
        the form.
    """

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
    """
    Allows a user to add tags to their profile.

    Handles both GET and POST requests. On GET requests, it displays a form
    pre-filled with the user's current tags. On POST requests, it processes the
    form submission to add the given tags to the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): the id of the user whose tags are to be added

    Returns:
        HttpResponse: A redirect to the user's profile page if the tag addition
        is successful, otherwise renders the tag addition page with the form.
    """
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
