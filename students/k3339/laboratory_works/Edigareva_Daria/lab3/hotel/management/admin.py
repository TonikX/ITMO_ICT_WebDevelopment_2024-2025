from django.contrib import admin

from management.models import Room, Client, Booking, Staff, CleaningSchedule, CleaningConfirmation

# Register your models here.
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Booking)
admin.site.register(Staff)
admin.site.register(CleaningSchedule)
admin.site.register(CleaningConfirmation)
