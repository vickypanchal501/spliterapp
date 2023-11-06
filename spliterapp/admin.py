
from django.contrib import admin
from .models import Group
class GroupMember(admin.ModelAdmin):
    list_display = ["id","name","creator" ]
admin.site.register(Group,GroupMember)
# admin.site.register(Group)
