from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import Owner, Auto_owner, Auto, Document

class CarOwnerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality', 'date_of_birth', 'first_name', 'last_name')}),
    )

admin.site.register(Owner, CarOwnerAdmin)
admin.site.register(Auto_owner)
admin.site.register(Auto)
admin.site.register(Document)


