"""
Admin panel for Event, EventParticipant and EventAttachment models
"""
from django.contrib import admin
from .models import Event, EventParticipant, EventAttachment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'type', 'scheduled_date', 'stream_session_id', 'active')

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user', 'active', 'type')

@admin.register(EventAttachment)
class EventAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id','attachment_cloud_id', 'attachment_name', 'active', 'type', 'event')