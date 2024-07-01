from rest_framework import serializers
from .models import Like, Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'img', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class PostDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'content', 'img', 'created_at', 'user_name', 'comment_count', 'like_count']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'post']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'post']