from django.contrib import admin

from .models import Flight, Reservation, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'user', 'rating', 'comment_date')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure', 'arrival', 'gate_number')
    search_fields = ('flight_number', 'airline')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat_number', 'ticket_number')
    list_filter = ('flight',)
    search_fields = ('user__username', 'ticket_number', 'flight__flight_number')
    autocomplete_fields = ['user', 'flight']
    fields = ('user', 'flight', 'seat_number', 'ticket_number')
