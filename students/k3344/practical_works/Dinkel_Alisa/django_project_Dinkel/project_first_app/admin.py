from django.contrib import admin
from project_first_app.models import CarOwner, Ownership, DriverLicense, Car


admin.site.register(CarOwner)
admin.site.register(Ownership)
admin.site.register(DriverLicense)
admin.site.register(Car)
