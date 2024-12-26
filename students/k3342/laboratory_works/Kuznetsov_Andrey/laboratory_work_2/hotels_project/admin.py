from django.contrib import admin
from .models import Hotel, Room, RoomType, Reservation, Review, Client

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Client)
