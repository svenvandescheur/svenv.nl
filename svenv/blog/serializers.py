from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from .models import Category, Image, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = ImageSerializer()
    author = UserSerializer()

    class Meta:
        model = Post
