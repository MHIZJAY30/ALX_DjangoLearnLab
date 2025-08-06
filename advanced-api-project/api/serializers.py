from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model, ensuring all fields are serialized.
    Includes custom validation for publication_year.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model, including a nested list
    of books written by the author using BookSerializer.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
