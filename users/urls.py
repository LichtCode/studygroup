from django.urls import path
from .views import register, update_profile, login, profile_detail, logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('update-profile/', update_profile, name='update_profile'),
    path('profile/<int:user_id>/', profile_detail, name='profile'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
]
