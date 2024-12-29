from django.contrib import admin

from .models import Client, Room, Staff, Stay, CleaningSchedule, CleaningExecution

admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Staff)
admin.site.register(Stay)
admin.site.register(CleaningSchedule)
admin.site.register(CleaningExecution)
