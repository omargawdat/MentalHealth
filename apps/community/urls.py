from django.urls import path
from .views import LikeView, PostCommentsView, PostListView, CreatePostView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', CreatePostView.as_view(), name='post-create'),
    path('posts/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comments/', PostCommentsView.as_view(), name='post-comments'),
    path('likes/', LikeView.as_view(), name='like-create-delete'),
]
