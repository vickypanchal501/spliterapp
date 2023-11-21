
from django.db import models
# from django.contrib.auth.models import User
from account.models import CustomUser
class Group(models.Model):
    name = models.CharField(max_length=255 )
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='group_members', blank=True)
    
    def __str__(self) -> str:
        return '{}'.format((self.name))
class Expense(models.Model):
    description = models.CharField(max_length=255)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    split_with = models.ManyToManyField(CustomUser, related_name='expenses_involved')
    split_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_payer' )
    amount_paid_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_lent_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    paid_by_name = models.CharField(max_length=255, blank=True, null=True)
    
    
    
    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        # Set the name of the user who paid before saving the expense
        self.paid_by_name = self.paid_by.username
        super().save(*args, **kwargs)