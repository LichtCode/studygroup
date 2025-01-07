from django.urls import path
from . import views

urlpatterns = [
    path("schedule-session/", views.schedule_session, name="schedule_session"),
    path("notifications/", views.notifications, name="notifications"),
    path("study-sessions/", views.study_sessions, name="study_sessions"),
]
