from django.contrib import admin
from .models import CarOwner, Car, Possesion, DriverLicence

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Possesion)
admin.site.register(DriverLicence)
