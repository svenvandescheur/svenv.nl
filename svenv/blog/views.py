from django.views import generic
from blog.models import Blog


class ListView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        """
        Gets a list of Blog items in newest first order
        """
        return Blog.objects.order_by('date').reverse()
