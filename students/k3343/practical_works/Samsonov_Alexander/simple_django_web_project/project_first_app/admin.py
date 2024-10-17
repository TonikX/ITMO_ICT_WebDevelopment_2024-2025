from django.contrib import admin
from .models import Owner, Owns, Car, Drivers_license

# Register your models here.
admin.site.register(Owner)
admin.site.register(Owns)
admin.site.register(Car)
admin.site.register(Drivers_license)

