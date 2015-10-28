__author__ = 'taiowawaner'

from django import forms

from .models import Comment


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text', 'user', 'path',)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}),)
