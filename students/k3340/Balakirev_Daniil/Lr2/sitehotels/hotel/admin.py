from django.contrib import admin
from .models import Hotel, Room, Booking, Review, RoomType, User

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)