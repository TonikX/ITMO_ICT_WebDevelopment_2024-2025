from django.contrib import admin

from hotel_app.models import RoomType, RoomPriceHistory, Room, Client, Reservation, EmployeePosition, EmploymentContract, \
    Employee, CleaningSchedule

admin.site.register(RoomType)
admin.site.register(RoomPriceHistory)
admin.site.register(Room)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(EmployeePosition)
admin.site.register(EmploymentContract)
admin.site.register(Employee)
admin.site.register(CleaningSchedule)
