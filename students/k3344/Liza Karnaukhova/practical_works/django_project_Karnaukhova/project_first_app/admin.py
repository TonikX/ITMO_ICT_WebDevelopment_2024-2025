from django.contrib import admin

from project_first_app.models import Owner, Ownership, DriverLicense, Car

admin.site.register(Owner)
admin.site.register(Ownership)
admin.site.register(DriverLicense)
admin.site.register(Car)
