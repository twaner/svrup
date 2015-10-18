"""srvup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^staff/$', 'srvup.views.staff_home', name='staff'),
    # videos
    url(r'^(?P<id>\d+)/$', 'videos.views.video_detail', name='video_detail'),
    url(r'^videos/$', 'videos.views.video_list', name='video_list'),

    # url(r'^$', TemplateView.as_view(template_name='base.html'), name='home')
]

# auth login/logout
urlpatterns += patterns('srvup.views',
    url(r'^login/$', 'auth_login', name='login'),
    url(r'^logout/$', 'auth_logout', name='logout'),
)