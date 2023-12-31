# models.py

from django.db import models
from account.models import CustomUser
from django.db.models import Sum
<<<<<<< HEAD
from decimal import Decimal
=======
>>>>>>> vicky

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
    split_amount = models.DecimalField(max_digits=10, decimal_places=2  ,null=True )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
<<<<<<< HEAD
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
=======
    percentages = models.JSONField(default=dict, blank=True, null=True)
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

>>>>>>> vicky
        owes_dict = {}
        for user in self.split_with.all():
            if user != self.paid_by:
                owes_dict[user] = self.split_amount
<<<<<<< HEAD
        return owes_dict

    def save(self, *args, **kwargs):
        self.paid_by_name = self.paid_by.username
        super().save(*args, **kwargs)


=======

        return owes_dict
    
    def save(self, *args, **kwargs):
        # Set the name of the user who paid before saving the expense
        self.paid_by_name = self.paid_by.username
        super().save(*args, **kwargs)

>>>>>>> vicky
         # Calculate amount lent (or owed) by the user for users not involved


class RepaymentDetail(models.Model):
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repayment_payer')
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='repayment_payee')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.payer} paid {self.amount} to {self.payee} in {self.group}"
<<<<<<< HEAD

    
=======
    # @property
    # def record_transaction(self, payer, payee, amount, group ):
    #     self.transactions = {}
    #     if payer not in self.transactions:
    #         self.transactions[payer] = {}
    #     if payee not in self.transactions[payer]:
    #         self.transactions[payer][payee] = 0
    #     self.transactions[payer][payee] += amount
    #     return transactions
>>>>>>> vicky

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

<<<<<<< HEAD
        cls.objects.create(payer=payer, payee=payee, group=group, amount=amount)

=======
        cls.objects.create(payer=payer, payee=payee, group=group, amount=amount)
>>>>>>> vicky
