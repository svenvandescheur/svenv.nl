from django.contrib.auth.models import User
from django.db import models
from subprocess import call


class BaseModel():
    def save(self):
        try:
            call(['varnishadm', 'ban', 'req.url ~ /'])
        except(OSError):
            print("Could not clear varnish cache")
        return models.Model.save(self)


class Category(BaseModel, models.Model):
    """
    Category model

    Categories contain posts
    """
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField()
    modified = models.DateTimeField(auto_now=True)


class Post(BaseModel, models.Model):
    """
    Post model

    Posts are written by Django users
    Posts live in a category
    Posts contain an image
    """
    def __str__(self):
        return self.short_title

    author = models.ForeignKey(User)
    category = models.ForeignKey('Category')
    image = models.ForeignKey('Image')
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField()
    modified = models.DateTimeField(auto_now=True)


class Image(BaseModel, models.Model):
    """
    Image model

    This class contains meta information about images
    It's primary use is to provide posts with images
    """
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    url = models.ImageField(upload_to='media/%Y/%m/%d', width_field='width', height_field='height')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Page(BaseModel, models.Model):
    """
    Page model

    Pages are simple (web) pages
    Pages are written by Django users
    Pages contain an image
    """
    def __str__(self):
        return self.path

    author = models.ForeignKey(User)
    image = models.ForeignKey('Image')
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    position = models.IntegerField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField()
    navigation = models.BooleanField()
    modified = models.DateTimeField(auto_now=True)