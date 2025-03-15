from django.contrib import admin
from .models import Airline, Aircraft, Places, Races, Review, Bookings, Ticket

models = [
    Airline,
    Aircraft,
    Places,
    Races,
    Review, Bookings, Ticket
]

for model in models:
    admin.site.register(model)