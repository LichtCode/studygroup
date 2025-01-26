from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from users.models import CustomUser

@login_required
def chat_rooms(request):
    """
    Renders a page displaying all the chat rooms a user is a member of.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML page with the list of chat rooms.
    """
    user = request.user
    rooms = user.chatrooms.all()
    return render(request, "chatroom/chat_rooms.html", {"rooms": rooms})

@login_required
def chat_room(request, room_id):
    """
    Renders a page displaying all the messages in a given chat room and the other user in the chat room.

    Args:
        request (HttpRequest): The HTTP request object.
        room_id (int): The id of the chat room to render.

    Returns:
        HttpResponse: A rendered HTML page with the list of messages and the other user.
    """
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.members.all():
        return redirect("dashboard")
    other_member = room.members.exclude(id=request.user.id).first()
    messages = room.messages.order_by("timestamp")
    user = request.user
    context = {
        'room': room,
        'messages': messages,
        'other_member': other_member,
        'user': user,
    }
    return render(request, "chatroom/chat_room.html", context)

@login_required
def user_chatroom(request, user_id):
    """
    Creates a chatroom between the current user and another user if one doesn't exist, and redirects to that chatroom.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The id of the other user to create a chatroom with.

    Returns:
        HttpResponse: A redirect to the chatroom.
    """
    current_user = request.user
    other_user = get_object_or_404(CustomUser, id=user_id)

    if current_user == other_user:
        return redirect('dashboard')

    chatroom = ChatRoom.get_or_create_chatroom(current_user, other_user)

    return redirect('chat_room', room_id=chatroom.id)