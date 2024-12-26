from django.contrib import admin
from .models import Owner, Car, Ownership, DriverLicense, User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )

admin.site.register(User, CustomUserAdmin)


admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)
