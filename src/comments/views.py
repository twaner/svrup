from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect


from .forms import CommentForm
from .models import Comment
from notifications.signals import notify
from videos.models import Video

@login_required
def comment_thread(request, id):
    comment = Comment.objects.get(id=id)
    form = CommentForm(None)
    context = {
        'comment_form': form,
        'comment': comment,
    }
    return render(request, 'comments/comment_thread.html', context=context)

@login_required
def comment_create_view(request):
    # print("comment_create_view called")
    if request.method == "POST" and request.user.is_authenticated():
        parent_id = request.POST.get('parent_id')
        video_id = request.POST.get('video_id')
        origin_path = request.POST.get('origin_path')
        try:
            video = Video.objects.get(id=video_id)
        except:
            video = None
        parent_comment = None
        # print('comment create view video: {0}'.format(video))
        if parent_id is not None:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                except:
                    parent_comment = None
                if parent_comment is not None and parent_comment.video is not None:
                    video = parent_comment.video
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            if parent_comment is not None:
                # parent comment exits; replying.
                print 'comment create view {0}'.format(parent_comment.get_affected_users())
                new_comment = Comment.objects.create_comment(user=request.user,
                                                             path=parent_comment.get_origin,
                                                             text=comment_text,
                                                             video=video,
                                                             parent=parent_comment)
                affected_users = parent_comment.get_affected_users()
                notify.send(request.user,
                            target=parent_comment,
                            action=new_comment,
                            recipient=parent_comment.user,
                            affected_users=affected_users,
                            verb='replied to')
                messages.success(request, "Thank you for your response, {0}. <a href='someline/item'>Item</a>".
                                 format(request.user.username), extra_tags='safe')
                return HttpResponseRedirect(parent_comment.get_absolute_url())

            else:
                # parent comment does not exits; new comment.
                new_comment = Comment.objects.create_comment(user=request.user,
                                                             path=origin_path,
                                                             text=comment_text,
                                                             video=video,
                                                             parent=None)
                messages.success(request, 'Thank you for your comment, {0}.'.format(request.user.username))
                notify.send(request.user,
                            recipient=request.user,
                            action=new_comment,
                            target=new_comment.video,
                            verb='commented on')
                return HttpResponseRedirect(new_comment.get_absolute_url())
        else:
            print("Invalid form")
            messages.error(request, "There was an error with your comment.")
            print('comment_create_view origin path {0}'.format(origin_path))
            return HttpResponseRedirect(origin_path)
    else:
        raise Http404