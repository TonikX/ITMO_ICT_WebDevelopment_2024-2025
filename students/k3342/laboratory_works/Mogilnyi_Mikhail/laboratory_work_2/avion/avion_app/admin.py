from django.contrib import admin
from .models import Flight, Reservation, Passenger, Review

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_city', 'arrival_city', 'departure_time', 'arrival_time')
    list_filter = ('airline', 'departure_city', 'arrival_city')
    search_fields = ('flight_number', 'airline')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat_number', 'reservation_date')
    search_fields = ('user__username', 'flight__flight_number')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'reservation', 'ticket_number')
    search_fields = ('first_name', 'last_name', 'ticket_number')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'review_date', 'rating')
    search_fields = ('user__username', 'flight__flight_number')
