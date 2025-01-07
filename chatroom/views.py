from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from users.models import CustomUser

@login_required
def chat_rooms(request):
    user = request.user
    rooms = user.chatrooms.all()
    return render(request, "chatroom/chat_rooms.html", {"rooms": rooms})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.members.all():
        return redirect("dashboard")
    other_member = room.members.exclude(id=request.user.id).first()
    messages = room.messages.order_by("timestamp")
    context = {
        'room': room,
        'messages': messages,
        'other_member': other_member,
    }
    return render(request, "chatroom/chat_room.html", context)

@login_required
def user_chatroom(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(CustomUser, id=user_id)

    if current_user == other_user:
        return redirect('dashboard')

    chatroom = ChatRoom.get_or_create_chatroom(current_user, other_user)

    return redirect('chat_room', room_id=chatroom.id)