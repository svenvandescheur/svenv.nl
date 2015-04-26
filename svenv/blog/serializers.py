from rest_framework import serializers, viewsets
from models import Category, Image, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class PostSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Post
