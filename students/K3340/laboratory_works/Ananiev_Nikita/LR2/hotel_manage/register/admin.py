from django.contrib import admin

from .models import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import AccountCreationForm, AccountChangeForm


class AccountAdmin(BaseUserAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    model = HotelBaseAccount

    list_display = ('email', 'firstname', 'lastname', 'birth_date', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_active', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'birth_date')}),
    )
    add_fieldsets = (
        (None, {'fields': ('firstname', 'lastname', 'email', 'birth_date', 'password1', 'password2', 'is_staff')}),
    )

    search_fields = ('email', 'firstname', 'lastname')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(HotelBaseAccount, AccountAdmin)