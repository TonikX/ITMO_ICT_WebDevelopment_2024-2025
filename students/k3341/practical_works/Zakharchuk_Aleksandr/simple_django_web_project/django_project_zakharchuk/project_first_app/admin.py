from django.contrib import admin

from project_first_app import models

admin.site.register(models.Owner)
admin.site.register(models.DriverLicense)
admin.site.register(models.Car)
admin.site.register(models.Ownership)
