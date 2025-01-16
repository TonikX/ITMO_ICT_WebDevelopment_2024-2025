from django.contrib import admin

from .models import Flight, Airline, Gate, Ticket, FlightReview, TicketReservation


admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(Gate)
admin.site.register(Ticket)
admin.site.register(TicketReservation)
admin.site.register(FlightReview)
