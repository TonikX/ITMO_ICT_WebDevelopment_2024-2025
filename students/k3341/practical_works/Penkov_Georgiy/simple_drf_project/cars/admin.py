from django.contrib import admin
from cars.models import CarOwner, DrivingLicense, Car, Ownership

admin.site.register(CarOwner)
admin.site.register(DrivingLicense)
admin.site.register(Car)
admin.site.register(Ownership)
