from django.contrib import admin
from .models import StudySession, Notification

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date_time', 'created_by', 'get_participants')
    list_filter = ('date_time', 'created_by')
    search_fields = ('topic', 'created_by__username', 'participants__username')
    ordering = ('-date_time',)

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
    message_preview.short_description = 'Message Preview'