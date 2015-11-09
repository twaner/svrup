from django.db import models
from django.core.urlresolvers import reverse
import datetime

from accounts.models import MyUser
from videos.models import Video
# Create your models here.


class CommentManager(models.Manager):

    def all(self):
        return super(CommentManager, self).filter(active=True).filter(parent=None)

    def create_comment(self, user=None, text=None, path=None, video=None, parent=None):
        if not user:
            raise ValueError('A user is needed to comment.')
        if not path:
            raise ValueError('Must include a path when adding a comment.')
        comment = self.model(
            user=user,
            path=path,
            text=text
        )
        if video is not None:
            comment.video = video
        if parent is not None:
            comment.parent = parent
        comment.save(using=self.db)
        return comment


class Comment(models.Model):
    user = models.ForeignKey(MyUser)
    path = models.CharField(max_length=350)
    parent = models.ForeignKey('self', null=True, blank=True)
    video = models.ForeignKey(Video, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)\

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('comment_thread', kwargs={'id': self.id})

    @property
    def get_origin(self):
        return self.path

    @property
    def get_comment(self):
        return self.text

    @property
    def is_child(self):
        if self.parent is not None:
            return True
        else:
            return False

    @property
    def get_id(self):
        return self.id

    @property
    def get_children(self):
        if self.is_child:
            return None
        else:
            return Comment.objects.filter(parent=self)
    @property
    def comment_time(self):
        if self.updated is not None:
            return self.updated.strftime('%b %d %Y')
        else:
            return self.timestamp.strftime('%b %d %Y')