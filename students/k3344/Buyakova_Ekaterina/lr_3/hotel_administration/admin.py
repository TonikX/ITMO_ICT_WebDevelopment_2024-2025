from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Client, Staff, CleaningSchedule, Reservation, Report


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Добавляем кастомное поле "is_admin" в админку
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )

    # Настройки отображения в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'type', 'price_per_day', 'is_occupied')
    search_fields = ('number', 'type')
    list_filter = ('floor', 'type', 'is_occupied')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'last_name', 'first_name', 'city')
    search_fields = ('passport_number', 'last_name', 'first_name')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'profession')
    search_fields = ('last_name', 'first_name', 'profession')


@admin.register(CleaningSchedule)
class CleaningScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'floor', 'day_of_week')
    list_filter = ('floor', 'day_of_week')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'room', 'check_in_date', 'check_out_date')
    list_filter = ('check_in_date', 'check_out_date')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('quarter', 'year', 'room', 'total_clients', 'total_income')
    list_filter = ('quarter', 'year')
