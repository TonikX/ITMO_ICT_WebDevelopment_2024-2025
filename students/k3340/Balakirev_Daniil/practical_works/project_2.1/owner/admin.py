from django.contrib import admin
from .models import CarOwner, DriversLicense, Car, OwnerShip

admin.site.register(CarOwner)
admin.site.register(DriversLicense)
admin.site.register(Car)
admin.site.register(OwnerShip)