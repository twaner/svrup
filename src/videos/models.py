from django.db import models
from django.core.urlresolvers import reverse


class VideoQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)


class VideoManager(models.Manager):
    def get_featured(self):
        # return super(VideoManager, self).filter(featured=True)
        return self.get_queryset().active().featured()

    def get_queryset(self):
        """
        Gets the Video models queryset.
        :return:  queryset of videos.
        """
        return VideoQuerySet(self.model, using=self._db)

    def all(self):
        """
        Overrides the default all queryset with a set of active Videos.
        :return: queryset of active Videos
        """
        return self.get_queryset().active()


class Video(models.Model):
    title = models.CharField(max_length=120)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=True)
    free_preview = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)

    objects = VideoManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'id': self.id})