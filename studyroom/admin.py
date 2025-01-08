from django.contrib import admin
from .models import  Group, Topic


# Registering the Group model
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'owner', 'description')
    search_fields = ('name', 'description', 'owner__username')
    filter_horizontal = ('members', 'tags')
