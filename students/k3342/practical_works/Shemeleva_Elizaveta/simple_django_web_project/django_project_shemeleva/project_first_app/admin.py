from django.contrib import admin
from .models import Car, Ownership, DriverLicense, User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('birth_date', 'passport_number', 'address', 'nationality')}),
    )

admin.site.register(User, CustomUserAdmin)
