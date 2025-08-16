from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth import get_user_model
from .models import Post, Tag, Comment

# Create your tests here.
class PostCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(title='Hello', content='Content', author=self.user)

    def test_create_requires_login(self):
        url = reverse('post-create')
        resp = self.client.get(url)
        self.assertNotEqual(resp.status_code, 200)  # should redirect to login

        self.client.login(username='alice', password='pass')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_author_can_edit(self):
        self.client.login(username='alice', password='pass')
        url = reverse('post-edit', args=[self.post.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_non_author_cannot_edit(self):
        self.client.login(username='bob', password='pass')
        url = reverse('post-edit', args=[self.post.pk])
        resp = self.client.get(url)
        # UserPassesTestMixin returns 403 or redirect — check as appropriate
        self.assertNotEqual(resp.status_code, 200)


User = get_user_model()

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pass')
        self.other = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(title='T', body='B', author=self.user)  # adapt fields to your Post model

    def test_create_comment_requires_login(self):
        resp = self.client.post(reverse('comment-create', kwargs={'post_pk': self.post.pk}), {'content': 'Hi'})
        # should redirect to login
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login/', resp['Location'])

    def test_post_comment_when_logged_in(self):
        self.client.login(username='u1', password='pass')
        resp = self.client.post(reverse('comment-create', kwargs={'post_pk': self.post.pk}), {'content': 'Nice post!'}, follow=True)
        self.assertContains(resp, 'Nice post!')
        self.assertEqual(self.post.comments.count(), 1)

    def test_only_author_can_edit_delete(self):
        comment = Comment.objects.create(post=self.post, author=self.other, content='X')
        self.client.login(username='u1', password='pass')
        # attempt edit page should be forbidden (UserPassesTestMixin returns 403)
        resp = self.client.get(reverse('comment-edit', kwargs={'pk': comment.pk}))
        self.assertIn(resp.status_code, (302, 403))  # depending on your login/redirect settings

class TagSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', 'u@example.com', 'pass')
        self.post1 = Post.objects.create(title='Django Tips', body='Learn forms', author=self.user)
        self.post2 = Post.objects.create(title='Python Tricks', body='Useful tips', author=self.user)
        django_tag = Tag.objects.create(name='django')
        tips_tag = Tag.objects.create(name='tips')
        self.post1.tags.add(django_tag, tips_tag)
        self.post2.tags.add(tips_tag)

    def test_view_by_tag(self):
        resp = self.client.get(reverse('posts-by-tag', args=['django']))
        self.assertContains(resp, 'Django Tips')
        self.assertNotContains(resp, 'Python Tricks')

    def test_search_by_title_body_tag(self):
        # search by word in title
        resp = self.client.get(reverse('search'), {'q': 'Django'})
        self.assertContains(resp, 'Django Tips')
        # search by tag name
        resp = self.client.get(reverse('search'), {'q': 'tips'})
        self.assertContains(resp, 'Django Tips')
        self.assertContains(resp, 'Python Tricks')
