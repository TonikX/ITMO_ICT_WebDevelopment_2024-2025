from django.contrib import admin

from hotels.models import Hotel, Room, Booking, Review

# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)