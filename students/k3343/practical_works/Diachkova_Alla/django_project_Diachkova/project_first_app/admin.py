from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Owner, Car, DriverLicense, Ownership


class CustomUserAdmin(UserAdmin):
    model = Owner
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'home_address', 'nationality')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_date', 'passport_number', 'home_address', 'nationality')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birth_date', 'passport_number', 'home_address', 'nationality', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )


admin.site.register(Owner, CustomUserAdmin)
admin.site.register(Car)
admin.site.register(DriverLicense)
admin.site.register(Ownership)
