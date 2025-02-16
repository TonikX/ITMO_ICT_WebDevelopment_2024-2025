from django.contrib import admin

from project_first_app.models import AutoOwner, DriverLicense, Ownership, Auto

admin.site.register(AutoOwner)
admin.site.register(Auto)
admin.site.register(DriverLicense)
admin.site.register(Ownership)
