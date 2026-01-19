from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CarOwnerUser, Car, Ownership, DrivingLicense


class CarOwnerUserAdmin(UserAdmin):
    # Добавляем новые поля в fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport', 'address', 'nationality', 'birth_date')
        }),
    )

    # Поля при создании пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport', 'address', 'nationality', 'birth_date', 'first_name', 'last_name', 'email')
        }),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'passport', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'passport', 'email']
    list_filter = ['is_staff', 'is_superuser', 'is_active']


admin.site.register(CarOwnerUser, CarOwnerUserAdmin)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'color', 'plate_number']
    search_fields = ['brand', 'model', 'plate_number']
    list_filter = ['brand', 'color']


@admin.register(Ownership)
class OwnershipAdmin(admin.ModelAdmin):
    list_display = ['owner', 'car', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['owner__first_name', 'owner__last_name', 'car__brand', 'car__model']


@admin.register(DrivingLicense)
class DrivingLicenseAdmin(admin.ModelAdmin):
    list_display = ['owner', 'license_number', 'type', 'issue_date']
    list_filter = ['type', 'issue_date']
    search_fields = ['owner__first_name', 'owner__last_name', 'license_number']