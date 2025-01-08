from django.contrib import admin

from .models import Hotel, Room, Review, Booking

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Booking)