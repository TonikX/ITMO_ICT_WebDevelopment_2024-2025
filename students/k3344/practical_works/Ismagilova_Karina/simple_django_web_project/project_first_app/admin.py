from django.contrib import admin
from .models import Owner, Car, Ownership, License

admin.site.register(Owner)
admin.site.register(License)
admin.site.register(Car)
admin.site.register(Ownership)
