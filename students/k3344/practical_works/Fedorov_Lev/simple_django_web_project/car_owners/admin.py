from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import Owner, Car, Ownership, License, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )


admin.site.register_reviewer(CustomUser)
admin.site.register_reviewer(Owner)
admin.site.register_reviewer(Car)
admin.site.register_reviewer(Ownership)
admin.site.register_reviewer(License)
