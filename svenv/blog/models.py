from django.contrib.auth.models import User
from django.db import models


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
    title = models.CharField(max_length=200)
    url_title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    """
    Category model
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)