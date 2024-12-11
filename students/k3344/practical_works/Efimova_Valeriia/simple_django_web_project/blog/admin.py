from .models import *
from django.contrib import admin
from .models import CarOwner


admin.site.register(Car)
admin.site.register(CarOwner)
admin.site.register(DriverLicense)
admin.site.register(Ownership)


class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'passport_number', 'address', 'nationality')
    search_fields = ('user__username', 'nationality')

admin.site.register(CarOwner, CarOwnerAdmin)
