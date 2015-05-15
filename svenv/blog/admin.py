from django.contrib import admin
from blog.models import Category, Post, Image, Page

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Page)