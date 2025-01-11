from django.contrib import admin
from school_app import models

admin.site.register(models.Classes)
admin.site.register(models.Teachers)
admin.site.register(models.Cabinets)
admin.site.register(models.Subjects)
admin.site.register(models.Teachings)
admin.site.register(models.Schedules)
admin.site.register(models.Students)
admin.site.register(models.Grades)