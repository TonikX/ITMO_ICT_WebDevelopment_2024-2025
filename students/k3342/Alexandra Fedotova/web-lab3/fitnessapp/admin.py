from django.contrib import admin
from .models import User, Profile, Workout, WorkoutPlan, BlogPost, ProgressTracking

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(WorkoutPlan)
admin.site.register(BlogPost)
admin.site.register(ProgressTracking)
