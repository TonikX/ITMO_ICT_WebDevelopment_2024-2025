from django.contrib import admin
from .models import CustomUser, Car, Ownership, DriverLicense
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'home_address', 'nationality')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)



