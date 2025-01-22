from django.contrib import admin

from insurance_app.models import Agent, CollectiveContract, IndividualContract, IndividualPayment, InsuredEmployee, \
    InsuredEventIndividual, InsuredEventEmployee, LaborContract, RiskCategory, Organization, EmployeePayment, \
    IndividualClient

# Register your models here.
admin.site.register(Agent)
admin.site.register(CollectiveContract)
admin.site.register(IndividualContract)
admin.site.register(IndividualPayment)
admin.site.register(IndividualClient)
admin.site.register(InsuredEmployee)
admin.site.register(InsuredEventIndividual)
admin.site.register(InsuredEventEmployee)
admin.site.register(LaborContract)
admin.site.register(RiskCategory)
admin.site.register(Organization)
admin.site.register(EmployeePayment)
