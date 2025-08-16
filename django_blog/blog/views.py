from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Tag
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q
from taggit.models import Tag


# Create your views here.
def home(request):
    return render(request, "blog/home.html")


def register(request):
    """
    Register view: shows a registration form and creates a new user.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account was created. You can now log in.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """
    Profile view: shows and lets authenticated users update their profile.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'blog/profile.html', context)


# List all posts (public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   
    context_object_name = 'posts'
    paginate_by = 10

# Detail view (public)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post' # helpful so template uses "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        # post.comments available due to related_name
        return context

# Create view (auth required)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # LoginRequiredMixin will redirect to settings.LOGIN_URL if not logged in

    def form_valid(self, form):
        # Auto set author to current user
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update view (only author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Delete view (only author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
            # Redirect to post detail and jump to comments section
            return redirect(reverse('post-detail', kwargs={'pk': post.pk}) + '#comments')
    # If GET or invalid form, redirect to post detail (you might instead re-render form with errors)
    return redirect(reverse('post-detail', kwargs={'pk': post.pk}))


# Create a comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']  # post_pk comes from URL
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk}) + '#comments'

# Edit a comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_edit.html'  

    def get_success_url(self):
        # redirect back to the post detail
        return reverse('post-detail', kwargs={'pk': self.object.post.pk}) + '#comments'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# Delete a comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk}) + '#comments'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

def posts_by_tag(request, tag_name):
    # Case-insensitive match
    posts = Post.objects.filter(tags__name__iexact=tag_name).distinct().order_by('-id')
    context = {
        'tag_name': tag_name,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)

def search(request):
    q = (request.GET.get('q') or '').strip()
    posts = Post.objects.none()
    if q:
        # If your content field is 'content', include that; if it's 'body', include that.
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q) |      # change to Q(content__icontains=q) if your field is 'content'
            Q(tags__name__icontains=q)
        ).distinct().order_by('-id')
    context = {'query': q, 'posts': posts}
    return render(request, 'blog/search_results.html', context)

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[tag])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag_slug')
        return context
