from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class StudySession(models.Model):
    topic = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_sessions")
    participants = models.ManyToManyField(User, related_name="sessions")

    def __str__(self):
        """
        Return a string representation of this StudySession.

        This string is used in the admin interface and elsewhere to identify
        this StudySession. It includes the topic and date/time of the session.

        :return: A string representation of this StudySession.
        :rtype: str
        """
        return f"{self.topic} on {self.date_time}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of this Notification.

        This string is used in the admin interface and elsewhere to identify
        this Notification. It includes the username of the user to whom the
        notification belongs.

        :return: A string representation of this Notification.
        :rtype: str
        """
        return f"Notification for {self.user.username}"
