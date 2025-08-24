from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    author_username = serializers.ReadOnlyField(source='author.username')
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'comments_count', 'like_count']
        read_only_fields = ['author', 'created_at', 'updated_at']

