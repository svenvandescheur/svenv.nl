from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    Category model

    Categories contain posts
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)


class Post(models.Model):
    """
    Post model

    Posts are written by Django users
    Posts live in a category
    Posts contain an image
    """
    def __str__(self):
        return self.url_title

    author = models.ForeignKey(User)
    category = models.ForeignKey('Category')
    image = models.ForeignKey('Image')
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
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
