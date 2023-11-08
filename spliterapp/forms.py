from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'split_with', 'split_amount','paid_by']
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['paid_by'].queryset = group.members.all()