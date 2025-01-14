from django.contrib import admin
from .models import CarOwner, Car, Possession, DrivingLicense

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Possession)
admin.site.register(DrivingLicense)
