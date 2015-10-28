from django.contrib import admin

# Register your models here.
from .models import Video, Category


class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Video
    list_display = ('title', 'id', 'slug', 'featured', 'updated')

admin.site.register(Category, CategoryAdmin)


class VideoAdmin(admin.ModelAdmin):
    class Meta:
        model = Video
    list_display = ('title', 'id', 'active', 'free_preview', 'updated')
    prepopulated_fields = {
        'slug': ('title',)
    }

admin.site.register(Video, VideoAdmin)
