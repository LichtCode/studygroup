from django.db import models
from users.models import CustomUser as User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional for user-specific chatrooms
    members = models.ManyToManyField(User, related_name="chatrooms")

    def __str__(self):
        """
        Returns the name of the chatroom if given, otherwise a string with the id of the chatroom.

        :return: The name of the chatroom if given, otherwise a string with the id of the chatroom.
        """
        return self.name if self.name else f"ChatRoom {self.id}"

    @staticmethod
    def get_or_create_chatroom(user1, user2):
        """
        Retrieves an existing chatroom for the given users or creates a new one.
        """
        # Retrieve a chatroom if it exists for these two users
        chatroom = ChatRoom.objects.filter(members=user1).filter(members=user2).distinct().first()
        if not chatroom:
            # Create a new chatroom if one doesn't exist
            chatroom = ChatRoom.objects.create()
            chatroom.name = f"{user1.username} and {user2.username}"
            chatroom.members.add(user1, user2)
            chatroom.save()
        return chatroom


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):        
        """
        Return a string representation of this Message.

        This string is used in the admin interface and elsewhere to identify
        this Message. It includes the username of the user who sent the
        message and the first 20 characters of the message content.

        :return: A string representation of this Message.
        :rtype: str
        """
        return f"{self.sender.username}: {self.content[:20]}"
