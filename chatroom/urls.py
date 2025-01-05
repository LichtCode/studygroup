from django.urls import path
from .views import chat_rooms, create_chat_room, chat_room

urlpatterns = [
    path("chat-rooms/", chat_rooms, name="chat_rooms"),
    path("create-chat-room/", create_chat_room, name="create_chat_room"),
    path("chat-room/<int:room_id>/", chat_room, name="chat_room"),
]
