from django.contrib import admin
from project_first_app.models import Owner, Car, License, Ownership

# Register your models here.
admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(License)
admin.site.register(Ownership)