from django.db import models

# Create your models here.
from django.db import models
import datetime

class Author(models.Model):
    """
    Author model to store the name of book authors.
    One Author can have many Books.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book model stores title, publication year, and
    links each book to one author via ForeignKey.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
