from django.urls import path
from .views import home
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', home, name='home'),
     path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    path('profile/', views.profile, name='profile'),


    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/update/', views.post_update, name='post_update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

     # existing post urls...
    # Create comment on a post
    path('posts/<int:post_pk>/comments/new/', views.comment_create, name='comment-create'),
    # Edit a comment
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-edit'),
    # Delete a comment
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]

