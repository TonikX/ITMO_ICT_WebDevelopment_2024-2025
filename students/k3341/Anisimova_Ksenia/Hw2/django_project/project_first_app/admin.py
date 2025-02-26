from django.contrib import admin
from .models import carOwner, car, possession, driver_license
from django.contrib.auth.admin import UserAdmin


admin.site.register(carOwner, UserAdmin)
admin.site.register(car)
admin.site.register(possession)
admin.site.register(driver_license)