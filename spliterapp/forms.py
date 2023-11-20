from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    split_amount_per_user = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['split_with'] = forms.ModelMultipleChoiceField(
            queryset=group.members.all(),
            widget=forms.CheckboxSelectMultiple,
        )
    class Meta:
        model = Expense
<<<<<<< HEAD
        fields = ['description', 'split_with', 'split_amount','paid_by']
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['paid_by'].queryset = group.members.all()
=======
<<<<<<< HEAD
<<<<<<< HEAD
        fields = ['description', 'split_with', 'split_amount','paid_by']
    def __init__(self, group, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['paid_by'].queryset = group.members.all()
=======
        fields = ['description', 'amount', 'date']
>>>>>>> parent of dfdcf37 (this is commit today add expense in admin07/11/2023)
=======
        fields = ['description', 'split_with', 'split_amount']
>>>>>>> parent of 0701fcf (this is today commit enhance ui 08/11/20123)
>>>>>>> vikas
