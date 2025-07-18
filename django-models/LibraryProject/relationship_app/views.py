from django.shortcuts import render
from .models import Book

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


from django.views.generic.detail import DetailView
from .models import Library

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html' 
    context_object_name = 'library'

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View

# Register view
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
        return render(request, 'relationship_app/register.html', {'form': form})


# Login view (you can also use LoginView from django)
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'


# Logout view
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import UserProfile

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


