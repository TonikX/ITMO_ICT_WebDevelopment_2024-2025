from django.contrib import admin
from .models import Car, CarOwner, DriverLicence, Ownership

admin.site.register(Car)
admin.site.register(CarOwner)
admin.site.register(DriverLicence)
admin.site.register(Ownership)
