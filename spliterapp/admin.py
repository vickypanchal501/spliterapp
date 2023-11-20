
from django.contrib import admin
from .models import Group, Expense

class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator" ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> vikas
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'group', 'split_amount', 'created_by','split_amount_per_user')
    search_fields = ['description']


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
