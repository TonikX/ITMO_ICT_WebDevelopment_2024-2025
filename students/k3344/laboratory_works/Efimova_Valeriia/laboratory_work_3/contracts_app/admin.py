from django.contrib import admin
from .models import (
    Organization,
    Employee,
    Contract,
    Agent,
    InsuranceCase,
    EmploymentContract,
)


admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(Contract)
admin.site.register(Agent)
admin.site.register(InsuranceCase)
admin.site.register(EmploymentContract)
