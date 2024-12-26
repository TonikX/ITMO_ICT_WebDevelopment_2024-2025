from django.contrib import admin
from .models import Hotel, Room, Reservation, Review, RoomType

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Review)
