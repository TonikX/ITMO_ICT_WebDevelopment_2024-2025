from django.contrib import admin

from project_first_app.models import Car, Owner, Possession, DriveLicense, ExampleModel
from .models import ExampleModel

admin.site.register(ExampleModel)
admin.site.register(Car)
admin.site.register(DriveLicense)
admin.site.register(Possession)
admin.site.register(Owner)