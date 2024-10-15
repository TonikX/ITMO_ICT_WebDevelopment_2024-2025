from django.contrib import admin

from project_hotel_app.models import Hotel, Reservation, Room

admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Room)
