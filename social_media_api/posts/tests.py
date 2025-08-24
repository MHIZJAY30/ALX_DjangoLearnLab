from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

# Create your tests here.
User = get_user_model()

class FollowFeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='alice', password='pass')
        self.u2 = User.objects.create_user(username='bob', password='pass')
        self.u3 = User.objects.create_user(username='carol', password='pass')
        # posts by bob and carol
        Post.objects.create(author=self.u2, title='Post B', body='B')
        Post.objects.create(author=self.u3, title='Post C', body='C')

    def test_follow_and_feed(self):
        self.client.login(username='alice', password='pass')
        # follow bob only
        resp = self.client.post(reverse('follow-user', args=[self.u2.pk]))
        self.assertEqual(resp.status_code, 200)
        # fetch feed
        resp = self.client.get(reverse('feed'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # depending on pagination; if list directly:
        titles = [item['title'] for item in data]
        self.assertIn('Post B', titles)
        self.assertNotIn('Post C', titles)


class LikeNotificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(title='T', body='B', author=self.u2)
        self.client.login(username='u1', password='pass')

    def test_like_creates_notification(self):
        url = reverse('post-like', args=[self.post.pk])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.u1).exists())
        notifs = Notification.objects.filter(recipient=self.u2, actor=self.u1, verb__icontains='liked')
        self.assertTrue(notifs.exists())

    def test_unlike_removes_like(self):
        self.client.post(reverse('post-like', args=[self.post.pk]))
        resp = self.client.post(reverse('post-unlike', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.u1).exists())
