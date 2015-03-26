from django.shortcuts import render
from django.views import generic
from blog.models import Blog

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        return Blog.objects.order_by('date').reverse()