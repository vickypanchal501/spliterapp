
from django.db import models
# from django.contrib.auth.models import User
from account.models import CustomUser
class Group(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='group_members', blank=True)

    def __str__(self) -> str:
        return self.name