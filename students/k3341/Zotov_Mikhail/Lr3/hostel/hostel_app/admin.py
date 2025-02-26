from django.contrib import admin
from .models import *

admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(ClientRoom)
admin.site.register(Employee)
admin.site.register(FloorSchedule)
admin.site.register(CleaningAssignment)
