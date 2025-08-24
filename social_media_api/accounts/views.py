from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer, SimpleUserSerializer

# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        })


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)
        token_key = resp.data['token']
        token = Token.objects.get(key=token_key)
        user = token.user
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    if request.user.is_following(target):
        return Response({'detail': 'Already following.'}, status=status.HTTP_200_OK)
    request.user.follow(target)
    return Response({'detail': 'Followed.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    if not request.user.is_following(target):
        return Response({'detail': 'Not following.'}, status=status.HTTP_200_OK)
    request.user.unfollow(target)
    return Response({'detail': 'Unfollowed.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_following_list(request):
    users = request.user.following.all()
    serializer = SimpleUserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_followers_list(request):
    users = request.user.followers.all()
    serializer = SimpleUserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)
