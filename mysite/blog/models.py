from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=1000, blank=False)
    publish = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
