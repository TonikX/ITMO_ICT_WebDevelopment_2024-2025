from django.contrib import admin
from project_first_app.models import Owner, Car, DriverLicense, Ownership

admin.site.register(Owner)
admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)
