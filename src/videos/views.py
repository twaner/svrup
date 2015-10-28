from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Video, Category
from comments.models import Comment
from comments.forms import CommentForm

@login_required
def video_detail(request, cat_slug, video_slug):
    print("VIDEO DETAIL")
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        print('vid detail cat slug except')
        raise Http404
    try:
        obj = Video.objects.get(slug=video_slug)
        comments = obj.comment_set.all()  # Comment.objects.filter(video=object)
        comment_form = CommentForm(request.POST or None)
        parent_comment = None
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            if parent_id is not None:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                except ObjectDoesNotExist:
                    parent_comment = None
                except:
                    parent_comment = None
            print('video detail parent_comment.get_comment {0}'.format(parent_comment))
            comment_text = comment_form.cleaned_data['comment']
            new_comment = Comment.objects.create_comment(user=request.user, path=request.get_full_path(),
                                                         text=comment_text, video=obj, parent=parent_comment)
            new_comment.save()
            # return render(request, 'videos/video_detail.html', {"obj": obj, 'cat': cat, 'comments': comments})
            return HttpResponseRedirect(obj.get_absolute_url())
        return render(request, 'videos/video_detail.html', {"obj": obj, 'cat': cat, 'comments': comments,                                                            'comment_form': comment_form})
    except:
        print('in main except')
        # raise Http404


def category_list(request):
    queryset = Category.objects.all()
    context = {
        "queryset": queryset,
    }
    print('category_list {0}'.format(queryset[0].id))
    return render(request, 'videos/video_list.html', context)


@login_required
def category_detail(request, cat_slug):
    try:
        obj = Category.objects.get(slug=cat_slug)
        queryset = obj.video_set.all()
        return render(request, "videos/video_list.html", {"obj": obj, 'queryset': queryset})
    except:
        raise Http404


'''
def video_edit(request):
    return render(request, 'video_detail.html', {})


def video_create(request):
    return render(request, 'video_detail.html', {})

'''