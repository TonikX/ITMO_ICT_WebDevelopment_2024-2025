from django.contrib import admin

from .models import Owner, Ownership, DriverLicense, Car

admin.site.register(Owner)
admin.site.register(Ownership)
admin.site.register(DriverLicense)
admin.site.register(Car)
