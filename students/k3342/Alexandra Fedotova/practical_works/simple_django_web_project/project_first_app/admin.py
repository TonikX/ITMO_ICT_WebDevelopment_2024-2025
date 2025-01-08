from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CarOwner, Car, Ownership, IDCard

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'passport_number', 'home_address', 'nationality', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(IDCard)
