from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

# BookViewSet handles CRUD operations on Book model.
# Only authenticated users can access these endpoints.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
