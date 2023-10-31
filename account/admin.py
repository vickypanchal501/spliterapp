from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# admin.site.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username','email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2'),
    #     }),
    # )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
# admin.site.register(U)
# admin.site.register(CustomUser, CustomUserAdmin)
