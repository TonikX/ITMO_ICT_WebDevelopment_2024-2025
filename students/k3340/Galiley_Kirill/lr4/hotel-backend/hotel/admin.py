from django.contrib import admin
from .models import Room, Client, Stay, Staff, CleaningSchedule

admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Stay)
admin.site.register(Staff)
admin.site.register(CleaningSchedule)
