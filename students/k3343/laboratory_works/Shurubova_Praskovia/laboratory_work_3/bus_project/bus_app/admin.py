from django.contrib import admin
from .models import *

admin.site.register(Bus)
admin.site.register(BusAssignment)
admin.site.register(Driver)
admin.site.register(DriverSchedule)
admin.site.register(Maintenance)
admin.site.register(Route)
