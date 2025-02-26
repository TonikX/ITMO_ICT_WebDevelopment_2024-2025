from django.contrib import admin
from .models import CarOwner, DriversLicense, Car, Ownership

admin.site.register(CarOwner)
admin.site.register(DriversLicense)
admin.site.register(Car)
admin.site.register(Ownership)