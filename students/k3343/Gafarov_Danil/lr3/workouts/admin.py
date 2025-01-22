from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Step)
admin.site.register(Tag)
admin.site.register(Workout)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Done)
admin.site.register(Routine)