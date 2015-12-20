from .base import *
from django.conf.urls.static import static

urlpatterns += static('/', document_root='../')
