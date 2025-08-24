from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_set',
        blank=True
    )
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers_set',
        blank=True
    )

    def follow(self, user):
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def __str__(self):
        return self.username

