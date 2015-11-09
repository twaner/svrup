__author__ = 'taiowawaner'

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Comment


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text', 'user', 'path',)


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Add your comment or reply."})
    )
    # comment = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}),)

    def __init__(self, data=None, files=None, **kwargs):
        super(CommentForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Comment', css_class='btn btn-primary',))