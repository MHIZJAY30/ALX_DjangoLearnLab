from django.urls import path
from .views import RegisterView, CustomObtainAuthToken, ProfileView, FollowUserView, UnfollowUserView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', views.my_following_list, name='my-following'),
    path('followers/', views.my_followers_list, name='my-followers'),
]

