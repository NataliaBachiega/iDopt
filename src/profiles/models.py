from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


class VerificationCode(models.Model):
    email: str = models.EmailField(unique=True)
    code: str = models.CharField(max_length=6, unique=True)
    enabled: bool = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


class IdoptUser(AbstractBaseUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    biography = models.TextField(blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']
