
from django.db import models
# from django.contrib.auth.models import User
from account.models import CustomUser
from django.db.models import Sum

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
    total_amount_paid_by_activeuser = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_lent_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_paid_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    paid_by_name = models.CharField(max_length=255, blank=True, null=True)
    
    
    
    def __str__(self):
        return self.description
    
    @property
    def owes(self):
        # Calculate owes and return a dictionary of members and their corresponding owed amounts
        # For example, if you have a field named 'split_amount' that represents the owed amount,
        # and 'split_with' is a ManyToManyField representing users involved in the expense,
        # you could use something like this:

        owes_dict = {}
        for user in self.split_with.all():
            if user != self.paid_by:
                owes_dict[user] = self.split_amount

        return owes_dict
    
    def save(self, *args, **kwargs):
        # Set the name of the user who paid before saving the expense
        self.paid_by_name = self.paid_by.username
        super().save(*args, **kwargs)

         # Calculate amount lent (or owed) by the user for users not involved


