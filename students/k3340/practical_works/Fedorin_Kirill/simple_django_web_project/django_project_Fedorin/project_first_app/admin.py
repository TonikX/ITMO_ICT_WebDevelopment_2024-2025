from django.contrib import admin

from project_first_app.models import Car, CarOwner, DriverLicense, Ownership

# Register your models here.


admin.site.register(CarOwner)
admin.site.register(Ownership)
admin.site.register(Car)
admin.site.register(DriverLicense)
