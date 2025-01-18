from django.contrib import admin
from .models import Flight, Reservation, Review


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('number', 'airline', 'departure', 'arrival', 'flight_type', 'gate')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat_number')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'user', 'date', 'rating')
