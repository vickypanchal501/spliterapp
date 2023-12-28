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
<<<<<<< HEAD
<<<<<<< HEAD
    description = models.CharField(max_length=255)
=======
    description = models.CharField( max_length=250)
    amount = models.IntegerField(default=0)
>>>>>>> vikas
=======
    description = models.CharField(max_length=255)
>>>>>>> vikcy
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    split_with = models.ManyToManyField(CustomUser, related_name='expenses_involved')
    split_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_payer' )
    split_amount_per_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
=======
>>>>>>> vikas
=======
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_payer' )
    split_amount_per_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
>>>>>>> vikcy
=======
    paid_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses_payer')
    total_amount_paid_by_activeuser = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_lent_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_paid_by_user = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    paid_by_name = models.CharField(max_length=255, blank=True, null=True)

>>>>>>> vicky
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


         # Calculate amount lent (or owed) by the user for users not involved


class RepaymentDetail(models.Model):
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repayment_payer')
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repayment_payee')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.payer} paid {self.amount} to {self.payee} in {self.group}"

    

    @classmethod
    def record_repayment(cls, payer, payee, group, amount):
        # Check if payer is a CustomUser instance
        if not isinstance(payer, CustomUser):
            try:
                payer = CustomUser.objects.get(username=payer)
            except CustomUser.DoesNotExist:
                raise ValueError(f"CustomUser with username {payer} does not exist.")
        
        # Check if payee is a CustomUser instance
        if not isinstance(payee, CustomUser):
            try:
                payee = CustomUser.objects.get(username=payee)
            except CustomUser.DoesNotExist:
                raise ValueError(f"CustomUser with username {payee} does not exist.")

        cls.objects.create(payer=payer, payee=payee, group=group, amount=amount)

