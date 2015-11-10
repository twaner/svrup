from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.urlresolvers import reverse
from django.db import models

from .signals import notify


class NotificationQuerySet(models.QuerySet):
    def get_user(self, user):
        return self.filter(recipient=user)

    def mark_all_read(self, recipient):
        qs = self.unread().get_user(recipient)
        qs.update(read=True)

    def mark_all_unread(self, recipient):
        qs = self.read().get_user(recipient)
        qs.update(read=False)

    def mark_targetless(self, user):
        qs = self.read().get_user(user)
        qs_no_target = qs.filter(target_object_id=None)
        if qs_no_target:
            qs_no_target.update(read=True)

    def unread(self):
        return self.filter(read=False)

    def read(self):
        return self.filter(read=True)

    def recent(self):
        return self.unread()[:5]


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def get_all_unread(self, user):
        return self.get_queryset().get_user(user).unread()

    def get_all_read(self, user):
        return self.get_queryset().get_user(user).read()

    def all_for_user(self, user):
        self.get_queryset().mark_targetless(user)
        return self.get_queryset().get_user(user)


class Notification(models.Model):
    # user
    sender_content_type = models.ForeignKey(ContentType, related_name='notify_sender')
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey('sender_content_type', 'sender_object_id')

    verb = models.CharField(max_length=255)

    action_content_type = models.ForeignKey(ContentType, related_name='notify_action', null=True, blank=True)
    action_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey('action_content_type', 'action_object_id')

    target_content_type = models.ForeignKey(ContentType, related_name='notify_target', null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # sender = models.ForeignKey()
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):

        try:
            target_url = self.target_object.get_absolute_url()

        except:
            target_url = None
        context = {
            'sender': self.sender_object,
            'verb': self.verb,
            'action': self.action_object,
            'target': self.target_object,
            'target_url': target_url,
            'verify_read': reverse('notifications_read', kwargs={'id': self.id}),
        }
        if self.target_object:
            if self.action_object and target_url:
                return '%(sender)s %(verb)s <a href="%(verify_read)s?next=%(target_url)s">%(target)s</a> with %(action)s' % context
            if self.action_object and not target_url:
                return '%(sender)s %(verb)s %(target)s with %(action)s' % context
            return '%(sender)s %(verb)s %(target)s' % context
        return '%(sender)s %(verb)s' % context
        # return '{0} {1} {2} {3}'.format(context['sender'], context['verb'], context['action'], context['target'])


def new_notification(sender, *args, **kwargs):
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    verb = kwargs.pop('verb')
    # target = kwargs.pop('target', None)
    # action = kwargs.pop('action', None)
    new_note = Notification(
        recipient=recipient,
        verb=verb,  # smart text
        sender_content_type=ContentType.objects.get_for_model(sender),
        sender_object_id=sender.id,
    )

    for option in ('target', 'action'):
        obj = kwargs.pop(option, None)
        if obj is not None:
            setattr(new_note, '{0}_content_type'.format(option), ContentType.objects.get_for_model(obj))
            setattr(new_note, '{0}_object_id'.format(option), obj.id)
    new_note.save()
notify.connect(new_notification)

"""
taiowa (AUTH_USER_MODEL)
has commented ('verb')
with a Comment(id=v) ) (instance action_object)
on your Comment(id=m) (targeted instance)
so now you should know about it (AUTH_USER_MODEL)
"""