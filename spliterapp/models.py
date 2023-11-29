# models.py

from django.db import models
from account.models import CustomUser
from django.db.models import Sum
from decimal import Decimal

class Group(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='group_members', blank=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    split_with = models.ManyToManyField(CustomUser, related_name='expenses_involved')
    split_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_payer')
    total_amount_paid_by_activeuser = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_lent_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_paid_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    paid_by_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description

    @property
    def owes(self):
        owes_dict = {}
        for user in self.split_with.all():
            if user != self.paid_by:
                owes_dict[user] = self.split_amount
        return owes_dict

    def save(self, *args, **kwargs):
        self.paid_by_name = self.paid_by.username
        super().save(*args, **kwargs)
