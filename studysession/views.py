from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StudySession, Notification
from chatroom.models import ChatRoom

@login_required
def schedule_session(request):
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
    user_notifications = request.user.notifications.filter(is_read=False)
    return render(request, "studysession/notifications.html", {"notifications": user_notifications})

@login_required
def study_sessions(request):
    sessions = request.user.sessions.all()
    return render(request, "studysession/study_sessions.html", {"sessions": sessions})
