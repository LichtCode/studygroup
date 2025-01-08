import uuid
from django.db import models
from users.models import CustomUser
from chatroom.models import ChatRoom
from django.db import models
from users.models import Tag
import random
import string



# Create your models here.


def generate_unique_id():
    return str(uuid.uuid4())[:8]

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group_id = models.CharField(max_length=8, unique=True, default=generate_unique_id)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(CustomUser, related_name='study_groups', blank=True)
    tags = models.ManyToManyField(Tag, related_name='group_tags', blank=True)
    chat_room = models.OneToOneField(ChatRoom, on_delete=models.CASCADE, related_name='group', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure a ChatRoom is created and linked when a Group is created.
        """
        is_new = self.pk is None  # Check if this is a new group
        if is_new:
            # Create a ChatRoom first to avoid a second save
            chat_room = ChatRoom.objects.create(name=f"Group Chat: {self.name}")
            chat_room.members.add(self.owner)
            chat_room.save()
            self.chat_room = chat_room
        super().save(*args, **kwargs)  # Save again to link the chat_room

    def add_member_to_group(self, user):
        """
        Adds a member to the group and to the associated chatroom.
        """
        self.members.add(user)  # Add user to the group
        if self.chat_room:  # Add user to the associated chatroom if it exists
            self.chat_room.members.add(user)
            self.chat_room.save()



class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    interested_users = models.ManyToManyField(CustomUser, related_name="interested_topics")
    tags = models.ManyToManyField(Tag, related_name="topics")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
