from django.contrib import admin

from hotel_app.models import Employee, EmployeeSchedule, Client, Reservation, Room

admin.site.register(Employee)
admin.site.register(EmployeeSchedule)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Room)