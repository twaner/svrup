from django.contrib import admin
from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display = ['__str__', 'id', 'text', 'path', 'parent', 'parent']

admin.site.register(Comment, CommentAdmin)