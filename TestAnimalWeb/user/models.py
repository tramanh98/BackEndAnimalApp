
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.URLField()
    phone = models.CharField(max_length = 15, blank=True)
    def __str__(self):
        return self.username
