from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404

from .forms import CommentForm
from .models import Comment


@login_required
def comment_thread(request, id):
    comment = Comment.objects.get(id=id)
    form = CommentForm(None)
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'comments/comment_thread.html', context=context)

@login_required
def comment_create_view(request):
    if request.method == "POST" and request.user.is_authenticated():
        form = CommentForm(request.POST or None)
        if form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id is not None:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                except:
                    parent_comment = None
            comment_text = form.cleaned_data['comment']
            if parent_comment is not None:
                new_comment = Comment.objects.create_comment(user=request.user, path=parent_comment.get_origin,
                                                             text=comment_text, video=parent_comment.video, parent=parent_comment)
            else:
                return
                # new_comment = Comment.objects.create_comment(user=request.user, path=parent_comment.get_origin,
                #                                              text=comment_text, video=parent_comment.video, parent=parent_comment)
            return # comment origin
    else:
        raise Http404