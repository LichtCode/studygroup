from django.urls import path
from .views import create_topic, user_dashboard, select_topics, find_matches, group_detail

urlpatterns = [
    path('create-topic/', create_topic, name='create_topic'),
    path('dashboard/', user_dashboard, name='dashboard'),
    path("select-topics/", select_topics, name="select_topics"),
    path("find-matches/", find_matches, name="find_matches"),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
]
