from blog.models import Category, Image, Post, Page
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_text
from django.views import generic
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.utils import formatting
import serializers


class BaseBlogView():
    """
    Base class for Blog views
    """
    media_url = settings.MEDIA_URL

    def is_in_debug_mode(self):
        """
        Method use to expose DEBUG setting to templates
        """
        return settings.DEBUG

    def get_media_url(self):
        """
        Method used to expose media url to templates
        """
        return self.media_url


class CategoryView(BaseBlogView, generic.ListView):
    """
    Shows a list of posts (e.g. home page)
    """
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

    def get_queryset(self):
        """
        Gets a list of Posts in the selected category limited to REST_FRAMEWORK['PAGE_SIZE']
        If no category is selected (home page) no category filtering is performed
        """
        category_name = self.kwargs['category_name']
        limit = settings.REST_FRAMEWORK['PAGE_SIZE']

        if category_name == '':
            return Post.objects.all().order_by('date').reverse()[:limit]

        category = get_object_or_404(Category, name=category_name)
        print category_name
        return Post.objects.filter(category=category).order_by('date').reverse()[:limit]



class PostView(BaseBlogView, generic.DetailView):
    """
    Shows a specific post
    """
    queryset = Post.objects.all()
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        """
        Finds the correct post by category_name and url_title
        """
        category = Category.objects.get(name__icontains=self.kwargs['category_name'])
        return get_object_or_404(Post, category=category, url_title__icontains=self.kwargs['url_title'])


class PageView(BaseBlogView, generic.DetailView):
    """
    Shows a specific page
    """
    queryset = Page.objects.all()
    model = Page
    template_name = 'blog/page.html'

    def get_object(self):
        """
        Finds the correct page by page_path
        If no page is found, it attempts to load a category
        """
        path = self.kwargs['page_path']
        return get_object_or_404(Page, path__icontains=path)


class BaseBlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Base class for viewsets
    """
    ordering_fields = ('__all__')


    def get_serializer_class(self):
        """
        Returns serializer class based on model name
        """
        return getattr(serializers, self.model.__name__ + 'Serializer')

    def get_view_description(self, html=False):
        """
        Fetches the docstring from the model and uses it as description
        """
        description = self.model.__doc__
        description = formatting.dedent(smart_text(description))
        if html:
            return formatting.markup_description(description)
        return description


class PostViewSet(BaseBlogViewSet):
    """
    Api viewset for post
    Supports HTML rendering
    """
    model = Post
    ordering = 'id'
    queryset = Post.objects.all()
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)
    template_name = 'blog/list.html'
