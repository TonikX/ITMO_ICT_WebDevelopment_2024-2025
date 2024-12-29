from django.contrib import admin

from hotel_app.models import Employee, Floor, Room, RoomType, Schedule


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin): ...


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin): ...


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin): ...


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]
