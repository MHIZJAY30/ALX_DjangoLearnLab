from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

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
