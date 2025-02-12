from django.contrib import admin
from .models import Owner, Ownership, Car, License, CustomUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(License)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
