from django.contrib import admin

from .models import (
    InsuranceAgency, Agent, EmploymentContract, Organization,
    Employee, Position, Contract, InsuranceCase, CustomUser,
)
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_filter = ('groups', 'role')


admin.site.register(InsuranceAgency)
admin.site.register(Agent)
admin.site.register(EmploymentContract)
admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Contract)
admin.site.register(InsuranceCase)
admin.site.register(CustomUser, CustomUserAdmin)
