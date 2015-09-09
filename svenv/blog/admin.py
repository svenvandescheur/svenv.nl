from blog.models import Category, Post, Image, Page
from django.contrib import admin
from django.db import models
from epiceditor.widgets import AdminEpicEditorWidget


class MarkdownAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminEpicEditorWidget(themes={'editor': 'epic-light.css', 'preview': 'github.css'})},
    }

admin.site.register(Category)
admin.site.register(Post, MarkdownAdmin)
admin.site.register(Image)
admin.site.register(Page, MarkdownAdmin)