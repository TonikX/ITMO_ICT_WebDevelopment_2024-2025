from django.contrib import admin
from .models import CarOwner
from .models import Car
from .models import Ownership
from .models import DriverLicense


# Register your models here.
admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Ownership)
admin.site.register(DriverLicense)

