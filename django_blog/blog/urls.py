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

    # Create comment on a post
    path('post/<int:pk>/comments/new/', views.comment_create, name='comment-create'),
    # Edit a comment
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    # Delete a comment
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # tags
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),

     # View posts by a specific tag (string param)
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),

    # Search endpoint that uses ?q=...
    path('search/', views.search, name='search'),
]
