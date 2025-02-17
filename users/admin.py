from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'address', 'phone_number', 'profile_image']  # Show profile_image
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address', 'phone_number', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('address', 'phone_number', 'profile_image')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
