from django.contrib import admin
from .models import CarOwner, Car, Ownership, DriverLicence, User

admin.site.register((CarOwner, Car, Ownership, DriverLicence, User))
