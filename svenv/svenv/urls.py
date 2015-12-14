from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('blog.urls')),
]
