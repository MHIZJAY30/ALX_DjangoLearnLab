from django import forms
from .models import Comment
from .models import Post, Tag
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
  # A virtual field to type tags as "news, django, tips"
    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g. django, tips, news)"
    )

    class Meta:
        model = Post
        # Include your existing editable fields + tags_input (not the m2m 'tags' directly)
        fields = ['title', 'content']  # author and published_date handled automatically
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current = list(self.instance.tags.values_list('name', flat=True))
            self.fields['tags_input'].initial = ', '.join(current)

    def clean_tags_input(self):
        raw = self.cleaned_data.get('tags_input', '')
        names = [t.strip() for t in raw.split(',') if t.strip()]
        # Normalize case; you can choose to keep original case if you prefer
        names = list(dict.fromkeys([n.lower() for n in names]))  # de-dupe & lower
        return names

    def save(self, commit=True):
        instance = super().save(commit=commit)
        names = self.cleaned_data.get('tags_input', [])
        # Create/get Tag objects and sync
        tag_objs = [Tag.objects.get_or_create(name=name)[0] for name in names]
        # If instance not committed yet, ensure it's saved before m2m
        if commit is False:
            instance.save()
        instance.tags.set(tag_objs)
        return instance

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


