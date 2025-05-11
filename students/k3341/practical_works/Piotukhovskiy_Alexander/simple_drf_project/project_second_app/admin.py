from django.contrib import admin
from .models import CarOwner, DrivingLicence, Car, Ownership

admin.site.register(CarOwner)
admin.site.register(DrivingLicence)
admin.site.register(Car)
admin.site.register(Ownership)