from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Owner, Car, Ownership


class CustomUserAdmin(UserAdmin):
    model = Owner
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birthday_date', 'passport_number', 'home_address', 'nationality')}),
    )


admin.site.register(Owner, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(Ownership)
