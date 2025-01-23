from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudySession, Notification
from chatroom.models import ChatRoom

@login_required
def schedule_session(request):
    """
    Schedule a new study session for a given chat room.

    **Request data**

        topic (str): the topic of the study session
        date_time (datetime): the date and time of the study session
        room_id (int): the ID of the chat room to schedule the study session for

    **Returns**

        A JSON response with a message indicating the success or failure of the
        operation. If the request is successful, a message of 'Study session
        scheduled successfully!' is returned. Otherwise, an appropriate error
        message is returned.

    **Status codes**

        200: the request was successful
        405: the request method was invalid (only POST is allowed)
    """
    print(request.user)
    if request.method == "POST":
        topic = request.POST["topic"]
        date_time = request.POST["date_time"]
        room_id = request.POST["room_id"]
        chat_room = ChatRoom.objects.get(id=room_id)
        session = StudySession.objects.create(topic=topic, date_time=date_time, created_by=request.user)

        # Notify participants
        for participant in chat_room.members.all():
            session.participants.add(participant)
            Notification.objects.create(
                user=participant,
                message=f"You've been added to a study session on {topic} at {date_time}."
            )
        return JsonResponse({'message': 'Study session scheduled successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def notifications(request):
    """
    Show all unread notifications for the user.

    **Context**
        notifications: a list of Notification objects that the user has not read
    """
    user_notifications = request.user.notifications.filter(is_read=False)
    return render(request, "studysession/notifications.html", {"notifications": user_notifications})

@login_required
def study_sessions(request):
    """
    Show all study sessions that the user is a part of.

    **Context**
        sessions: a list of StudySession objects that the user is a part of
    """

    sessions = request.user.sessions.all()
    return render(request, "studysession/study_sessions.html", {"sessions": sessions})
