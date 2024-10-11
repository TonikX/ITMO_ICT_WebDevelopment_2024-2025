from django.contrib import admin
from driving.models import Car, CarOwner, License, Ownership


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin): ...


@admin.register(Car)
class CarAdmin(admin.ModelAdmin): ...


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin): ...


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin): ...
