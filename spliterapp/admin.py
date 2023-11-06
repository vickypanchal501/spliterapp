
from django.contrib import admin
from .models import Group, Expense
class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator" ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)

class ExpenseDetail(admin.ModelAdmin):
    list_display = ["id","description","amount","created_by", "group_by","date" ]
admin.site.register(Expense,ExpenseDetail)