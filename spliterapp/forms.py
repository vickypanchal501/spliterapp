from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    split_amount_per_user = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    percentages = forms.JSONField(required=False)
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['split_with'] = forms.ModelMultipleChoiceField(
            queryset=group.members.all(),
            widget=forms.CheckboxSelectMultiple,
        )
    class Meta:
        model = Expense
        fields = ['description', 'split_with', 'split_amount','paid_by']
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['paid_by'].queryset = group.members.all()