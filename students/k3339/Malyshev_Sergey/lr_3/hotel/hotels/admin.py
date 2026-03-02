from django.contrib import admin
from .models import RoomType, Room, Guest, Booking, Employee, CleaningAssignment


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price_per_day')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'room_type', 'phone', 'is_active')
    list_filter = ('floor', 'room_type', 'is_active')
    search_fields = ('number', 'phone')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'passport', 'city')
    search_fields = ('last_name', 'first_name', 'passport', 'city')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'check_in', 'check_out', 'is_active')
    list_filter = ('check_in', 'check_out')
    search_fields = ('guest__last_name', 'guest__passport', 'room__number')
    date_hierarchy = 'check_in'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('last_name', 'first_name')


@admin.register(CleaningAssignment)
class CleaningAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'floor', 'get_day_of_week')
    list_filter = ('floor', 'day_of_week')
    search_fields = ('employee__last_name',)

    def get_day_of_week(self, obj):
        return obj.get_day_of_week_display()
    get_day_of_week.short_description = 'День недели'