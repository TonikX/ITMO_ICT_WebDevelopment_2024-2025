from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(CuratedList)