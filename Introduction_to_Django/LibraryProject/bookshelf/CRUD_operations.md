## CREATE
from bookshelf.models import Book  
book = Book(title="1984", author="George Orwell", publication_year=1949)  
book.save()  
# Output: Book object created successfully  

## RETRIEVE
book = Book.objects.get(id=1)  
print(book.title, book.author, book.publication_year)  
# Output: 1984 George Orwell 1949  

## UPDATE
book.title = "Nineteen Eighty-Four"  
book.save()  
print(book.title)  
# Output: Nineteen Eighty-Four  

## DELETE
book.delete()  
Book.objects.all()  
# Output: QuerySet [] → Book deleted successfully
