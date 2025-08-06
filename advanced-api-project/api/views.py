from django.shortcuts import render
from rest_framework import serializers

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
import datetime

# ListView - Anyone can view
class BookList(generics.ListAPIView):
    """
    View to list all books in the system.
    Publicly accessible.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# DetailView - Anyone can view
class BookDetail(generics.RetrieveAPIView):
    """
    View to retrieve a specific book by ID.
    Publicly accessible.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# CreateView - Only for authenticated users
class BookCreate(generics.CreateAPIView):
    """
    View to create a new book.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic can go here
        serializer.save()

# UpdateView - Only for authenticated users
class BookUpdate(generics.UpdateAPIView):
    """
    View to update an existing book.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure publication_year is not in future
        year = serializer.validated_data.get("publication_year", None)
        if year and year > datetime.datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        serializer.save()

# DeleteView - Only for authenticated users
class BookDelete(generics.DestroyAPIView):
    """
    View to delete an existing book.
    Only accessible by authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


from rest_framework import generics, filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add filter backends
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Define filterable fields
    filterset_fields = ['title', 'publication_year', 'author__name']

    # Define searchable fields
    search_fields = ['title', 'author__name']

    # Define orderable fields
    ordering_fields = ['title', 'publication_year']