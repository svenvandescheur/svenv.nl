from django.views import generic
from blog.models import Category, Post


class ListView(generic.ListView):
    template_name = 'blog/list.html'
    context_object_name = 'blog_list'

    def get_queryset(self):
        """
        Gets a list of Blog items in newest first order
        """
        category = self._get_category()
        print Post.objects.filter(category=category).order_by('date').reverse()
        return Post.objects.filter(category=category).order_by('date').reverse()

    def _get_category(self):
        """
        Attempts to get the category from url
        if no category name is given it defaults to the first category in database
        """
        if self.kwargs['category_name'] is not None:
            return Category.objects.get(name=self.kwargs['category_name'])
        else:
            return Category.objects.all()[:1].get()


class PostView(generic.DetailView):
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        """
        Finds the correct post by category_name and url_title
        """
        category = Category.objects.get(name__icontains=self.kwargs['category_name'])
        return Post.objects.get(category=category, url_title__icontains=self.kwargs['url_title'])