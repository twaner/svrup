from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect, redirect
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
            if next_url is not None:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect('/')

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

