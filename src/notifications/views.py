import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect

from .models import Notification
# Create your views here.

@login_required
def all(request):
    notifications = Notification.objects.all_for_user(request.user)

    context = {
        'notifications': notifications,
    }

    return render(request, 'notifications/all.html', context)


@login_required
def read(request, id):
    try:
        next = request.GET.get('next', None)
        notification = Notification.objects.get(id=id)
        print next
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
            if request is not None:
                print('notification read requst is not none next: {0}'.format(next))
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('notifications_all'))
        else:
            raise Http404
    except ValueError:
        return HttpResponseRedirect(reverse('notifications_all'))
    except:
        return HttpResponseRedirect(reverse('notifications_all'))


@login_required
def get_notifications_ajax(request):
    if request.is_ajax() and request.method == "POST":
        notifications = Notification.objects.all_for_user(request.user)#.recent()
        print "TEST"
        for i in notifications:
            print "NOTIFS GETLINK {0}".format(i.get_link)
        # notes = [n.get_link for n in notifications]
        notes = []
        for i in notifications:
            notes.append(i.get_link)
        print "lsit comp : {0}".format(notes)
        count = notifications.count()
        data = {
            'notifications': notes,
            'count': count,
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type='application/json')

