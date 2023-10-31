# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # You can add more custom fields as needed
    
    def __str__(self):
        return self.email
