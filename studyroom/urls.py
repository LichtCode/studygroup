from django.urls import path
from .views import create_topic

urlpatterns = [
    path('create-topic/', create_topic, name='create_topic'),
]
