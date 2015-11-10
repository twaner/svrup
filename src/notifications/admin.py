from django.contrib import admin

from .models import Notification

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    class Meta:
        model = Notification

    list_display = (
        'read', 'sender_content_type', 'sender_object_id', 'sender_object', 'verb', 'action_content_type',
        'action_object_id',
        'action_object', 'target_content_type', 'target_object_id', 'target_object', 'recipient')


admin.site.register(Notification, NotificationAdmin)

