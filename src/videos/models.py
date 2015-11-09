import urllib2
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify


# Querysets

class VideoQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

# Model Managers


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


DEFAULT_MESSAGE = "Check out this awesome video"


class Video(models.Model):
    title = models.CharField(max_length=120)
    embed_code = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    share_message = models.TextField(default=DEFAULT_MESSAGE)
    slug = models.SlugField(null=True, blank=True)
    active = models.BooleanField(default=True)
    free_preview = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    category = models.ForeignKey("Category", default=1)
    tags = GenericRelation('TaggedItem', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    objects = VideoManager()

    class Meta:
        unique_together = ('slug', 'category')

    def __str__(self):
        return self.title

    def get_share_message(self):
        get_full_url = '{0}{1}'.format(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
        return urllib2.quote('{0}{1}'.format(self.share_message, get_full_url))

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'video_slug': self.slug, 'cat_slug': self.category.slug})


def video_signal_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        slug_title = slugify(instance.title)
        new_slug = '{0} {1} {2}'.format(instance.title, instance.category, instance.id)
        try:
            obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
            instance.slug = slugify(new_slug)
            instance.save()
            print("exists and new slug created")
        except Video.DoesNotExist:
            instance.slug = slugify(instance.title)
            instance.save()
            print("slug created and moodel created")
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()
            print("slug created mult objects new slug")
        except TypeError:
            instance.slug = None


post_save.connect(video_signal_post_save_receiver, sender=Video)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
    title = models.CharField(max_length=120)
    slug = models.SlugField(default='abc', unique=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    tags = GenericRelation('TaggedItem', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'cat_slug': self.slug})


# class TaggedItem(models.Model):
    # category = models.ForeignKey(Category, null=True, blank=True)
    # video = models.ForeignKey(Category, null=True, blank=True)


class TaggedItem(models.Model):
    TAG_CHOICES = (
        ('python', 'python'),
        ('django', 'django'),
        ('css', 'css'),
        ('bootstrap', 'bootstrap'),
    )
    tag = models.SlugField(choices=TAG_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag
