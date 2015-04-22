from django.contrib.auth.models import User
from django.db import models
from exceptions import NotUniqueException


class Post(models.Model):
    """
    Post model

    Posts live in a category
    The combination url_title and category should be unique
    """
    def __str__(self):
        return self.url_title

    author = models.OneToOneField(User)
    category = models.ForeignKey('Category')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        """
        Override save to prevent duplicate paths
        """
        if Post.objects.filter(category=self.category, url_title__icontains=self.url_title):
            raise NotUniqueException('Another post with url_title %s already exists in category with name %s' % (self.url_title, self.category))
        super(Post, self).save(*args, **kwargs)


class Category(models.Model):
    """
    Category model
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)