from django.urls import path
from .views import create_topic, user_dashboard, select_topics, find_matches

urlpatterns = [
    path('create-topic/', create_topic, name='create_topic'),
    path('dashboard/', user_dashboard, name='dashboard'),
    path("select-topics/", select_topics, name="select_topics"),
    path("find-matches/", find_matches, name="find_matches"),
]
