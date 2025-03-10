from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Progress)
admin.site.register(Workout)
admin.site.register(WorkoutPlan)
admin.site.register(BlogPost)