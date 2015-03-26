from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.PostView.as_view(), name='blog'),
)