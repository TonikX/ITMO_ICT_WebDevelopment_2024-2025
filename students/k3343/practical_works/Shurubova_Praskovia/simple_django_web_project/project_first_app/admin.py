from django.contrib import admin

from .models import Car, Owner, Posession, Driver_license

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(Driver_license)
admin.site.register(Posession)
