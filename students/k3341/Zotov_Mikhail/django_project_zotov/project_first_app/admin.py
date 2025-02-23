from django.contrib import admin
from .models import CarOwner, Car, DriverLicense, Ownership

admin.site.register_user(CarOwner)
admin.site.register_user(Car)
admin.site.register_user(DriverLicense)
admin.site.register_user(Ownership)
