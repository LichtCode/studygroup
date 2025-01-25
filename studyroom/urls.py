from django.urls import path
from .views import add_topic, remove_topic, groups_list, create_topic, user_dashboard, select_topics, find_matches, group_detail, search_group, join_group, create_group, topics_list, landing_page

urlpatterns = [
    path('remove-topic/', remove_topic, name='remove_topic'),
    path('add-topic/', add_topic, name='add_topic'),
    path('create-topic/', create_topic, name='create_topic'),
    path('', landing_page, name='landing_page'),
    path('dashboard/', user_dashboard, name='dashboard'),
    path("select-topics/", select_topics, name="select_topics"),
    path("find-matches/", find_matches, name="find_matches"),
    path('group/<int:group_id>/', group_detail, name='group_detail'),
    path('group-search/', search_group, name='search_group'),
    path('join-group/', join_group, name='join_group'),
    path('create-group/', create_group, name='create_group'),
    path('topics/', topics_list, name='topics'),
    path('groups/', groups_list, name='groups'),
]
