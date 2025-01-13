from django.contrib import admin
from .models import Car
from .models import Affiliation
from .models import Owner
from .models import License


admin.site.register(Car)
admin.site.register(Affiliation)
admin.site.register(Owner)
admin.site.register(License)
