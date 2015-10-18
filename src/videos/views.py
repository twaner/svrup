from django.shortcuts import render, Http404
from .models import Video


def video_detail(request, id):
    try:
        obj = Video.objects.get(id=id)
        print(obj)
        return render(request, 'videos/video_detail.html', {"obj": obj})
    except:
        print("EXCEPT")
        raise Http404


def video_list(request):
    queryset = Video.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, 'videos/video_list.html', context)

'''
def video_edit(request):
    return render(request, 'video_detail.html', {})


def video_create(request):
    return render(request, 'video_detail.html', {})

'''