from django.contrib import admin
from .models import Car, Owner, Ownership, License

# Register your models here.
admin.site.register(Owner)
admin.site.register(License)
admin.site.register(Car)
admin.site.register(Ownership)