# relationship_app/query_samples.py

from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
author_name = "Chinua Achebe"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author.name}:", list(books_by_author))

# Query 2: List all books in a library
library_name = "Central Library"  
library = Library.objects.get(name=library_name)  
books_in_library = library.books.all()
for book in books_in_library:
    print(book.title)

# Query 3: Retrieve the librarian for a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
librarian = Librarian.objects.get(library=library)
print(f"Librarian for {library.name}:", librarian.name)
