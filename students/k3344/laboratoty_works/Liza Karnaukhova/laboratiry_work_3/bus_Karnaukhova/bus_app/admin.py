from django.contrib import admin
from .models import Bus, Route, BusDriver, WorkSchedule

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(BusDriver)
admin.site.register(WorkSchedule)
