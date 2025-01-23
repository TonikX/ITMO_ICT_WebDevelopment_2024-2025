from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Car, DrivingLicense, Ownership, CarOwner


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(CarOwner)
admin.site.register(DrivingLicense)
admin.site.register(Ownership)
