from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PostModel(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class LikeModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = 'like'
        verbose_name_plural = 'likes'
