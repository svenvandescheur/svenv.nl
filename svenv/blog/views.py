from blog.forms import ContactForm
from blog.models import Category, Image, Post, Page
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_text
from django.views import generic
from rest_framework import viewsets
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer
from rest_framework.utils import formatting
from socket import getfqdn
from . import serializers


class BaseBlogView():
    base_url = settings.BASE_URL
    blog_description = settings.BLOG_DESCRIPTION
    blog_title = settings.BLOG_TITLE
    language_code = settings.LANGUAGE_CODE
    media_url = settings.MEDIA_URL
    is_in_debug_mode = settings.DEBUG
    is_post = False

    def get_fqdn(self):
        """
        Method used to expose fqdn to templates
        """
        return getfqdn()

    def get_navigation(self):
        """
        Method used to expose navigation to templates
        """
        return Page.objects.filter(navigation=True, published=True).order_by('position')

    def get_pages(self):
        """
        Method used to expose pages to templates
        """
        return Page.objects.filter(published=True).order_by('position')


class CategoryView(BaseBlogView, generic.ListView):
    """
    Shows a list of posts (e.g. home page)
    """
    context_object_name = 'article_list'
    template_name = 'blog/category.html'

    def get_name(self):
        return self.get_property_or_default('name', 'Home')

    def get_description(self):
        return self.get_property_or_default('description', self.blog_description())

    def get_property_or_default(self, property, default):
        category_name = self.kwargs['category_name']
        if not category_name == '':
            category = Category.objects.get(name=category_name, published=True)
            return getattr(category, property)
        return default

    def get_queryset(self):
        """
        Gets a list of Posts in the selected category limited to REST_FRAMEWORK['PAGE_SIZE']
        If no category is selected (home page) no category filtering is performed
        """
        category_name = self.kwargs['category_name']
        limit = settings.REST_FRAMEWORK['PAGE_SIZE']

        if category_name == '':
            return Post.objects.filter(published=True, category__published=True).order_by('date').reverse()[:limit]

        category = get_object_or_404(Category, name=category_name, published=True)
        return Post.objects.filter(category=category, published=True).order_by('date').reverse()[:limit]


class PostView(BaseBlogView, generic.DetailView):
    """
    Shows a specific post
    """
    queryset = Post.objects.all()
    model = Post
    template_name = 'blog/post.html'

    def get_object(self):
        """
        Finds the correct post by category_name and short_title
        """
        category = get_object_or_404(Category, name__icontains=self.kwargs['category_name'], published=True)
        return get_object_or_404(Post, category=category, short_title__icontains=self.kwargs['short_title'], published=True)

    def get_context_data(self, **kwargs):
        """
        @Todo
        """
        context = super(PostView, self).get_context_data(**kwargs)

        try:
            context['next_post'] = self.object.get_next_by_date()
        except:
            context['next_post'] = None

        try:
            context['previous_post'] = self.object.get_previous_by_date()
        except:
            context['previous_post'] = None

        return context

    def is_post(self):
        """
        Returns whether the view belongs to a blog post
        """
        return True


class PageView(BaseBlogView, generic.DetailView):
    """
    Shows a specific page
    """
    context_object_name = 'post'
    queryset = Page.objects.all()
    model = Page
    template_name = 'blog/page.html'

    def get_object(self):
        """
        Finds the correct page by page_path
        If no page is found, it attempts to load a category
        """
        path = self.kwargs['page_path']
        return get_object_or_404(Page, path__icontains=path, published=True)


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
    queryset = Post.objects.filter(published=True, category__published=True).order_by('date').reverse()
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)
    template_name = 'blog/categoryajax.html'


class SearchPostViewSet(BaseBlogViewSet):
    """
    Api viewset for searching posts
    Uses value GET parameter 'query' to perform a basic search
    Supports HTML rendering
    """
    model = Post
    ordering = 'id'
    queryset = Post.objects.filter(published=True, category__published=True).order_by('date').reverse()
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)
    template_name = 'blog/categoryajax.html'

    def get_queryset(self):
        """
        Filters the queryset with the given search query
        """
        query = self.request.GET.get('query', '')
        queryset = super(SearchPostViewSet, self).get_queryset()

        for keyword in query.split(' '):
            keyword = keyword.strip()
            queryset = queryset.filter(content__icontains=keyword)
        return queryset


class ContactView(BaseBlogView, generic.edit.FormView):
    """
    Shows a page with a form
    """
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = settings.CONTACT_THANK_YOU_PAGE

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['post'] = self.get_page()
        return context

    def get_page(self):
        """
        Returns a page with content for this form
        """
        querySet = Page.objects.filter(path=settings.CONTACT_PAGE_PATH, published=True)
        if not len(querySet) == 0:
            return querySet[0]


class SiteMapView(BaseBlogView, generic.TemplateView):
    """
    Shows a xml sitemap for SEO
    """
    template_name = 'blog/sitemap.xml'

    def get_categories(self):
        return Category.objects.filter(published=True)

    def get_pages(self):
        return Page.objects.filter(published=True)

    def get_posts(self):
        return Post.objects.filter(published=True)
