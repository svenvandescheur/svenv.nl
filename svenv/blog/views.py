from django.views import generic
from blog.models import Category, Post


class ListView(generic.ListView):
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

    def get_queryset(self):
        """
        Gets a list posts in newest first order
        """
        if self.kwargs['category_name'] is not None:
            return Post.objects.filter(category=self.kwargs['category_name']).order_by('date').reverse()
        else:
            return Post.objects.all().order_by('date').reverse()


class PostView(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        """
        Finds the correct post by category_name and url_title
        """
        category = Category.objects.get(name__icontains=self.kwargs['category_name'])
        return Post.objects.get(category=category, url_title__icontains=self.kwargs['url_title'])
