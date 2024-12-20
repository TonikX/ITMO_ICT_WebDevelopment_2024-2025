from django.contrib import admin
from .models import (InsuranceAgency, Agent, EmploymentContract, Organization, Employee,
                     Position, Contract, InsuranceCase, CustomUser)

class InsuranceAgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency_info')
    list_filter = ('agents',)

class AgentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'passport_data', 'contact_info')
    search_fields = ('first_name', 'last_name', 'passport_data')
    list_filter = ('first_name', 'last_name')

class EmploymentContractAdmin(admin.ModelAdmin):
    list_display = ('agent', 'organization', 'start_date', 'end_date', 'salary')
    search_fields = ('agent__first_name', 'agent__last_name', 'organization__full_name')
    list_filter = ('organization', 'agent')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('code', 'full_name', 'short_name', 'address', 'bank_details', 'specialization')
    search_fields = ('full_name', 'short_name', 'code')
    list_filter = ('specialization',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'risk_category', 'payout_amount', 'position')
    search_fields = ('first_name', 'last_name', 'passport_data', 'risk_category')
    list_filter = ('position', 'risk_category')

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_staff')
    search_fields = ('name',)
    list_filter = ('is_staff',)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('agent', 'organization', 'start_date', 'end_date', 'total_sum', 'contract_type')
    search_fields = ('agent__first_name', 'agent__last_name', 'organization__full_name')
    list_filter = ('contract_type',)

class InsuranceCaseAdmin(admin.ModelAdmin):
    list_display = ('contract', 'date', 'reason', 'payout_decision', 'payout_amount')
    search_fields = ('contract__id', 'reason', 'payout_decision')
    list_filter = ('payout_decision',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'organization')
    search_fields = ('username', 'role', 'organization__full_name')
    list_filter = ('role',)

admin.site.register(InsuranceAgency, InsuranceAgencyAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(EmploymentContract, EmploymentContractAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(InsuranceCase, InsuranceCaseAdmin)
admin.site.register(CustomUser, CustomUserAdmin)