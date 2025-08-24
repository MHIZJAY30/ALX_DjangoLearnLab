from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, permissions, status,
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author']              
    search_fields = ['title', 'content']                
    ordering_fields = ['created_at', 'updated_at', 'title'] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post', 'author']              
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  

    def get_queryset(self):
        user = self.request.user
        following_qs = user.following.all()
        return Post.objects.filter(author__in=following_qs).order_by('-created_at')

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()  
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  

        like, created = Like.objects.get_or_create(user=request.user, post=post)  

        if created:
            Notification.objects.create(
                user=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    # Prevent duplicate likes
    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        return Response({'detail': 'Already liked.'}, status=status.HTTP_200_OK)

    if post.author != user:
        from notifications.models import Notification
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=str(post.pk)
        )
    return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    try:
        like = Like.objects.get(post=post, user=user)
        like.delete()
        return Response({'detail': 'Post unliked.'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)


