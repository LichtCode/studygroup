from django.contrib import admin
from .models import ChatRoom, Message

# Registering the ChatRoom model
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    filter_horizontal = ('members',)

# Registering the Message model
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom', 'sender', 'content', 'timestamp')
    search_fields = ('content', 'sender__username', 'chatroom__name')
    ordering = ('-timestamp',)