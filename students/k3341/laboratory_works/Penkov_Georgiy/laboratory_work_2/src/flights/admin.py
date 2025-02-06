from django.contrib import admin
from flights.models import Flight, Airline, PassengerRegistration, Feedback

admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(PassengerRegistration)
admin.site.register(Feedback)
