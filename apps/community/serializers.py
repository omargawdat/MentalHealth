from rest_framework import serializers

from .models import Like, Post, Comment
from ..authentication.serializers import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'img', 'created_at', 'user']
        read_only_fields = ['id', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(source='user.profile', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    created_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'content', 'img', 'created_at', 'user', 'comment_count', 'like_count', 'is_liked',
                  'created_by_current_user']

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return Like.objects.filter(user=user, post=obj).exists()

    def get_created_by_current_user(self, obj):
        user = self.context.get('request').user
        return obj.user == user


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
