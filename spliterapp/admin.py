
from django.contrib import admin
<<<<<<< HEAD
from .models import Group, Expense 
=======
from .models import Group, Expense ,RepaymentDetail
>>>>>>> vicky

class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator", ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> vikas
=======
>>>>>>> vikcy
class ExpenseAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('description', 'group', 'split_amount', 'created_by','paid_by_name','amount_paid_by_user', 'amount_lent_by_user','total_amount_paid_by_activeuser','owes',)
    search_fields = ['description']


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
admin.site.register(Expense, ExpenseAdmin)
=======
admin.site.register(Expense, ExpenseAdmin)
=======

class ExpenseDetail(admin.ModelAdmin):
    list_display = ["id","description","amount","created_by", "group_by","date" ]
admin.site.register(Expense,ExpenseDetail)
>>>>>>> parent of dfdcf37 (this is commit today add expense in admin07/11/2023)
>>>>>>> vikas
=======
admin.site.register(Expense, ExpenseAdmin)
>>>>>>> vikcy
=======
admin.site.register(Expense, ExpenseAdmin)
>>>>>>> vicky
=======
    list_display = ('description', 'group', 'split_amount', 'created_by','paid_by','percentages',"owes")
    search_fields = ['description']


admin.site.register(Expense, ExpenseAdmin)
class RepaymentDetailAdmin(admin.ModelAdmin):
    list_display = ["id","payer","payee","group","amount" ]
admin.site.register(RepaymentDetail,RepaymentDetailAdmin)

# class RepaymentMember(admin.ModelAdmin):
#     list_display = ["from_user","to_user","amount" ]
# admin.site.register(Repayment,RepaymentMember)
>>>>>>> vicky
