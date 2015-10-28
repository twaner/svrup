from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe

from videos.models import Video
from accounts.forms import RegistrationForm
from accounts.models import MyUser


def home(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password2']
        user = MyUser()
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()
        # email user
        # create user profile instance
        # HttpResponseRedirect(reverse('login'))
        return redirect('login')

    context = {
        'form': form,
        'action_value': '/',
        'submit_button_value': 'Register'
        # "videos": videos,
        # "embeds": embeds,
    }
    return render(request, 'form.html', context)


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