from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Country)
admin.site.register(Tour)
admin.site.register(Departure)
admin.site.register(Reservation)