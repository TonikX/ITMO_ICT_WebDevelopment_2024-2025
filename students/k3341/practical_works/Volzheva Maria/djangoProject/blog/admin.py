from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from djangoProject import settings

from .models import User
from .models import DriverLicense
from .models import Car
from .models import Ownership

admin.site.register(User, UserAdmin)
admin.site.register(DriverLicense)
admin.site.register(Car)
admin.site.register(Ownership)
