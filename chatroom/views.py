from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message

@login_required
def chat_rooms(request):
    user = request.user
    rooms = user.chatrooms.all()
    return render(request, "chatroom/chat_rooms.html", {"rooms": rooms})

@login_required
def create_chat_room(request):
    if request.method == "POST":
        room_name = request.POST["name"]
        room = ChatRoom.objects.create(name=room_name)
        room.members.add(request.user)
        return redirect("chat_rooms")

    return render(request, "chatroom/create_chat_room.html")

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.members.all():
        return redirect("chat_rooms")
    
    messages = room.messages.order_by("timestamp")
    return render(request, "chatroom/chat_room.html", {"room": room, "messages": messages})
