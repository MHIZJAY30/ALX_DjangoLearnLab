from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet


#Create router and register BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]


from rest_framework.authtoken.views import obtain_auth_token


# This endpoint provides token to users via username/password
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  
    path('', include(router.urls)),
]
