from django.urls import path
from .views import register, update_profile, login

urlpatterns = [
    path('register/', register, name='register'),
    path('update-profile/', update_profile, name='update_profile'),
    path('login/', login, name='login'),
]
