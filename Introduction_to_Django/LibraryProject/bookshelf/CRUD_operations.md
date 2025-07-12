## CREATE
from bookshelf.models import Book

new_book = Book.objects.create(title='1984', author='George Orwell', publication_year='1949')
# Output: Book object created successfully  

## RETRIEVE
books = Book.objects.get('1984') 
# Output: 1984 George Orwell 1949  

## UPDATE
book = Book.objects.get(title='1984') book.title = 'Nineteen Eighty-Four' book.save()
# Output: Nineteen Eighty-Four  

## DELETE
from bookshelf.models import Book book = Book.objects.get(title='1984') book.delete() 
# Output: QuerySet [] → Book deleted successfully
