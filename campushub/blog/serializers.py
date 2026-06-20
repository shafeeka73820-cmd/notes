from rest_framework import serializers
from .models import Category, Post, Comment
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author_name', 'category_name',
                  'status', 'created', 'updated']


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'author', 'author_name',
                  'category', 'category_name', 'status', 'created',
                  'updated', 'comment_count']
        read_only_fields = ['id', 'author', 'created', 'updated', 'slug']

    def get_comment_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'body', 'created']
        read_only_fields = ['id', 'author', 'created']
