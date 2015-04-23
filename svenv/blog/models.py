from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    Category model
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)


class Post(models.Model):
    """
    Post model

    Posts are written by Django users
    Posts live in a category
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
    Image to be used as header image in blog post
    """
    def __str__(self):
        return self.title

    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    width = models.IntegerField()
    height = models.IntegerField()
