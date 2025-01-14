from django.contrib import admin
from .models import Sport, Coach, Sportsman, SportHall, SportSection, SportSectionCoaches, Schedule

admin.site.register(Sport)
admin.site.register(Coach)
admin.site.register(Sportsman)
admin.site.register(SportHall)
admin.site.register(SportSection)
admin.site.register(SportSectionCoaches)
admin.site.register(Schedule)
