from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.utils.safestring import mark_safe
from videos.models import Video
from .forms import LoginForm


def auth_login(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        print("{0} {1}".format(username, password))
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

    context = {
        "form": form
    }
    return render(request, 'login.html', context)


@login_required#(login_url='/accounts/login/')
def home(request):
    name = "taiowa"
    videos = Video.objects.get_featured()
    embeds = [mark_safe(x.embed_code) for x in videos]
    context = {
        "name": name,
        "number": videos.count,
        "videos": videos,
        "embeds": embeds,
    }
    return render(request, 'home.html', context)


@login_required(login_url='/staff/login/')
def staff_home(request):
    context = {
    }
    return render(request, 'home.html', context)



'''
def home(request):
    if request.user.is_authenticated():
        name = "taiowa"
        videos = Video.objects.all()
        embeds = [mark_safe(x.embed_code) for x in videos]
        context = {
            "name": name,
            "number": videos.count,
            "videos": videos,
            "embeds": embeds,
        }
        return render(request, 'home.html', context)
    else:
        return HttpResponseRedirect('/login/')
'''