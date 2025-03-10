from django.contrib import admin

# Register your models here.
from .models import (
    CarOwner,
    DriverLicense,
    Car,
    Ownership,
)

admin.site.register(CarOwner)
admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)