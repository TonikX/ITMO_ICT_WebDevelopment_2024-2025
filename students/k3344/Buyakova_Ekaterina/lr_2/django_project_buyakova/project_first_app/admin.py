from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Car, Ownership

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(Ownership)
