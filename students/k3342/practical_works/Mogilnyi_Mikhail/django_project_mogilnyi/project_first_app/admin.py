from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CarOwner, Car, DrivingLicense, Ownership, User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('passport_number', 'address', 'nationality')}),
    )
    list_display = ('username', 'passport_number', 'address', 'nationality', 'is_staff')
    search_fields = ('username', 'passport_number', 'nationality')

admin.site.register(User, CustomUserAdmin)
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(DrivingLicense)
admin.site.register(Ownership)
