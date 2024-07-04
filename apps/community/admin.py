from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Post, Comment, Like


class CommentInline(TabularInline):
    model = Comment
    extra = 0
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('created_at',)


class LikeInline(TabularInline):
    model = Like
    extra = 0
    fields = ('user', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['content_preview', 'user_info', 'image_preview', 'comment_count', 'like_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'user__email']
    date_hierarchy = 'created_at'
    inlines = [CommentInline, LikeInline]

    fieldsets = (
        (None, {
            'fields': ('user', 'content', 'img')
        }),
        (_('Metadata'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)

    @display(description=_("Content"))
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    @display(description=_("User"), ordering="user__email")
    def user_info(self, obj):
        return f"{obj.user.email} ({obj.user.profile.first_name} {obj.user.profile.last_name})"

    @display(description=_("Image"))
    def image_preview(self, obj):
        if obj.img:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.img.url)
        return "No image"

    @display(description=_("Comments"), ordering="comment_count")
    def comment_count(self, obj):
        return obj.comment_count

    @display(description=_("Likes"), ordering="like_count")
    def like_count(self, obj):
        return obj.like_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            comment_count=Count('comments', distinct=True),
            like_count=Count('likes', distinct=True)
        )


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['content_preview', 'user_info', 'post_preview', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['content', 'user__email', 'post__content']
    date_hierarchy = 'created_at'

    @display(description=_("Content"))
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    @display(description=_("User"), ordering="user__email")
    def user_info(self, obj):
        return f"{obj.user.email} ({obj.user.profile.first_name} {obj.user.profile.last_name})"

    @display(description=_("Post"), ordering="post__content")
    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ['user_info', 'post_preview', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__email', 'post__content']
    date_hierarchy = 'created_at'

    @display(description=_("User"), ordering="user__email")
    def user_info(self, obj):
        return f"{obj.user.email} ({obj.user.profile.first_name} {obj.user.profile.last_name})"

    @display(description=_("Post"), ordering="post__content")
    def post_preview(self, obj):
        return obj.post.content[:50] + '...' if len(obj.post.content) > 50 else obj.post.content
