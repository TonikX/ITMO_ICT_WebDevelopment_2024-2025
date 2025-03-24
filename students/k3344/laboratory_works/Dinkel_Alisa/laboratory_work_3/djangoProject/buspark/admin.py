from django.contrib import admin
from .models import BusCategory, Bus, Driver, Route, Shift


admin.site.register(BusCategory)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(Shift)
