from django.db import models
from users.models import CustomUser
from django.db import models
from users.models import Tag
import random
import string



# Create your models here.

def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group_id = models.CharField(max_length=8, unique=True, default=generate_unique_id)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_groups')
    members = models.ManyToManyField(CustomUser, related_name='study_groups', blank=True)
    tags = models.ManyToManyField(Tag, related_name='group_tags', blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    interested_users = models.ManyToManyField(CustomUser, related_name="interested_topics")
    tags = models.ManyToManyField(Tag, related_name="topics")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
