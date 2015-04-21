from django.conf.urls import patterns, url
from blog.views import ListView, PostView

urlpatterns = patterns('',
    url(r'^(?P<category_name>[a-zA-Z0-9-_]+)?/?$', ListView.as_view(), name='list'),
    url(r'^(?P<category_name>[a-zA-Z0-9-_]+)/(?P<url_title>[a-zA-Z0-9-_]+)/?$', PostView.as_view(), name='post'),
)