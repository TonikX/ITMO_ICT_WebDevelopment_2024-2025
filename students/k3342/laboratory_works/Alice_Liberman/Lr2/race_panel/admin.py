from django.contrib import admin

# Register your models here.
from .models import Race, RaceTime

admin.site.register(Race)
admin.site.register(RaceTime)
