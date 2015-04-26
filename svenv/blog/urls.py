from django.conf.urls import patterns, include, url
from blog.views import ListView, PostView
from rest_framework import routers, serializers, viewsets
from views import PostViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<category_name>[a-zA-Z0-9-_]+)?/?$', ListView.as_view(), name='list'),
    url(r'^(?P<category_name>[a-zA-Z0-9-_]+)/(?P<url_title>[a-zA-Z0-9-_]+)/?$', PostView.as_view(), name='post'),
)
