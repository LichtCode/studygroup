
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='users', blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Returns a string representation of the Tag, which is its name.

        :return: The name of the Tag.
        """
        return self.name
