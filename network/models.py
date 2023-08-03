from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Author: {self.user} / Likes: {self.likes}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_set')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.post}'

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'


"""
class Tests(models.Model):
    url = models.CharField(max_length=255, blank=True, unique=True)
    order = models.FloatField(blank=True, null=True)
    theory = models.ForeignKey(Theory, on_delete=models.CASCADE, blank=True, null=True)
    testname = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(TestTypes, on_delete=models.CASCADE)
    topic = models.ForeignKey(TheoryTopics, on_delete=models.CASCADE)
    lvl = models.CharField(max_length=255)
    sentences = models.JSONField()
    answers = models.JSONField()
    explanation = models.JSONField(blank=True, null=True)
    options = models.JSONField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
"""
