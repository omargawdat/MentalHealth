from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Like, Post, Comment
from .serializers import LikeSerializer, PostDetailSerializer, PostSerializer, CommentSerializer

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostDetailSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatePostView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Set the user from the request
            return Response({'message': 'Post Created successfully', 'post': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('id')
        if not post_id:
            return Response({'detail': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id, user=request.user)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        post_id = request.data.get('id')
        if not post_id:
            return Response({'detail': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)

class CommentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'detail': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)  # Set the user and post from the request
            return Response({'message': 'Comment Created successfully', 'comment': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({'detail': 'Comment ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({'detail': 'Comment ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_200_OK)


class PostCommentsView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'detail': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class LikeView(APIView):
    def post(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'detail': 'Post ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'message': 'Like created successfully', 'like': LikeSerializer(like).data}, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({'message': 'Like deleted successfully'}, status=status.HTTP_200_OK)