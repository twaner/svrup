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
    url(r'^projects/$', 'videos.views.category_list', name='projects'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='project_detail'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<video_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
    # categories
    # url(r'^videos/$', 'videos.views.video_list', name='video_list'),
    # url(r'^(?P<cat_slug>[\w-]+/?P<id>\d+)/$', 'videos.views.video_detail', name='video_detail'),

    # url(r'^$', TemplateView.as_view(template_name='base.html'), name='home')
]
# auth login/logout
urlpatterns += patterns('accounts.views',
                        url(r'^login/$', 'auth_login', name='login'),
                        url(r'^logout/$', 'auth_logout', name='logout'),
)

# comment_thread
urlpatterns += patterns('comments.views',
                        url(r'^comment/(?P<id>\d+)$', 'comment_thread', name='comment_thread'),
                        url(r'^comment/create/$', 'comment_create_view', name='comment_create'),
)

# Notifications
urlpatterns += patterns('notifications.views',
                        url(r'^notifications/all/$', 'all', name='notifications_all'),
                        url(r'^notifications/ajax/$', 'get_notifications_ajax', name='get_notifications_ajax'),
                        url(r'^notifications/read/(?P<id>\d+)/$', 'read', name='notifications_read'),

)