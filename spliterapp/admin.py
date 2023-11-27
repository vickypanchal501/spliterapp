
from django.contrib import admin
from .models import Group, Expense 

class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator" ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'group', 'split_amount', 'created_by','paid_by_name','amount_paid_by_user', 'amount_lent_by_user','owes')
    search_fields = ['description']


admin.site.register(Expense, ExpenseAdmin)

