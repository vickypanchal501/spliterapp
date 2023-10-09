from django.db import models
import time 
import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionManager
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
# Create your models here.

class UserProfileManager(BaseUserManager):
    def creaet_user(self, email, name, password = None) -> "UserProfile":
        if not email:
            raise ValueError("invalid Email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using= self.db)
        return user

class UserProfile(AbstractBaseUser):
    "datebase models for user in system" 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=225, unique=True)
    name= models.CharField(max_length=225)
    is_active =models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   

    objects = UserProfileManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self) -> str:
        """
        Retrieve full name of user
        :return: str
        """
        return self.name

    def get_short_name(self) -> str:
        """
        Retrieve full name of user
        :return: str
        """
        return self.name

    def __str__(self) -> str:
        """
        Return String representation of User
        :return: str
        """
        return f"Email: {self.email}, Name:{self.name}"
