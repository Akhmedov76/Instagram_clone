from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=17)


class VerificationModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='verification')
    code = models.CharField(max_length=5)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email}-{self.code}'

    class Meta:
        verbose_name = 'verification'
        verbose_name_plural = 'verifications'
        ordering = ['-created_at']
        unique_together = ('user', 'code')

class FollowerModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='follower')
    follower = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'followers'
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
        unique_together = ('user', 'follower')
