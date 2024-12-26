from django.contrib import admin
from .models import Bus, Route, Driver, Schedule, Incident

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Driver)
admin.site.register(Schedule)
admin.site.register(Incident)
