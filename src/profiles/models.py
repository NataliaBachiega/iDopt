from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from knox.models import AuthToken


class IdoptUser(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    biography = models.TextField(blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']


class Device(models.Model):
    name: str = models.CharField(max_length=50)
    os: str = models.CharField(max_length=16)
    os_version: str = models.CharField(max_length=16)
    fcm_token: str = models.TextField()
    owner: IdoptUser = models.ForeignKey(IdoptUser, on_delete=models.CASCADE)
    token = models.ForeignKey(AuthToken, on_delete=models.CASCADE, null=True)


class VerificationCode(models.Model):
    email: str = models.EmailField(unique=True)
    code: str = models.CharField(max_length=6, unique=True)
    enabled: bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
