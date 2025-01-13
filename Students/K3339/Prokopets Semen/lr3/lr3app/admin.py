from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BusType, Bus, Driver, Route, WorkShift


admin.site.register(Driver)
admin.site.register(BusType)
admin.site.register(Route)
admin.site.register(WorkShift)
admin.site.register(Bus)