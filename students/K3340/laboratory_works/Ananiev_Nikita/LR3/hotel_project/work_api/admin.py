from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Contract)
admin.site.register(SalaryHistory)
admin.site.register(WorkSchedule)
