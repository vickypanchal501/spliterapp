
from django.contrib import admin
from .models import Group, Expense ,RepaymentDetail

class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator", ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'group', 'split_amount', 'created_by','paid_by','owes','percentages')
    search_fields = ['description']


admin.site.register(Expense, ExpenseAdmin)
class RepaymentDetailAdmin(admin.ModelAdmin):
    list_display = ["id","payer","payee","group","amount" ]
admin.site.register(RepaymentDetail,RepaymentDetailAdmin)

# class RepaymentMember(admin.ModelAdmin):
#     list_display = ["from_user","to_user","amount" ]
# admin.site.register(Repayment,RepaymentMember)