from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from comments.models import Comment
from .models import Video, Category, TaggedItem
from comments.forms import CommentForm

@login_required
def video_detail(request, cat_slug, video_slug):
    try:
        cat = Category.objects.get(slug=cat_slug)
    except:
        print('vid detail cat slug except')
        raise Http404
    try:
        obj = Video.objects.get(slug=video_slug)
        comments = obj.comment_set.all()  # Comment.objects.filter(video=object)
        # commented out when the GenericRelationship was added
        # content_type = ContentType.objects.get_for_model(obj) or None
        # tags = TaggedItem.objects.filter(content_type=content_type, object_id=obj.id)
        # content_type = obj.content_type or None
        # tags = obj.tags.all()
        # print('video_detail content_type: {0} tags: {1}'.format(content_type, obj.tags.all()))
        comment_form = CommentForm(None)
        return render(request, 'videos/video_detail.html', {"obj": obj, 'cat': cat, 'comments': comments,
                                                            'comment_form': comment_form})
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