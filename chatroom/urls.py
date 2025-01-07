from django.urls import path
from .views import chat_rooms, user_chatroom, chat_room

urlpatterns = [
    path("chat-rooms/", chat_rooms, name="chat_rooms"),
    path('chatroom/<int:user_id>/', user_chatroom, name='user_chatroom'),
    path("chat-room/<int:room_id>/", chat_room, name="chat_room"),
]
