from django import forms
from .models import Comment
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_photo']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # author and published_date handled automatically
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        if not content.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) > 2000:
            raise forms.ValidationError("Comment cannot be longer than 2000 characters.")
        return content
