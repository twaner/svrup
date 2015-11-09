from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
from .models import Video, Category, TaggedItem


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem


class TaggedItemAdmin(admin.ModelAdmin):
    class Meta:
        model = TaggedItem
    list_display = ('tag', 'content_type', 'object_id', 'content_object')

admin.site.register(TaggedItem, TaggedItemAdmin)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]

    class Meta:
        model = Category
    list_display = ('title', 'id', 'slug', 'featured', 'updated')

admin.site.register(Category, CategoryAdmin)


class VideoAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]

    class Meta:
        model = Video
    list_display = ('title', 'id', 'active', 'free_preview', 'updated')
    prepopulated_fields = {
        'slug': ('title',)
    }

admin.site.register(Video, VideoAdmin)



