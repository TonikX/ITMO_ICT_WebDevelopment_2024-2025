from django.contrib import admin
from .models import Hotel, RoomType, Room, Reservation, Review


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'is_checked_in', 'is_checked_out')
    list_filter = ('is_checked_in', 'is_checked_out')
    actions = ['check_in_guests', 'check_out_guests']

    def check_in_guests(self, request, queryset):
        queryset.update(is_checked_in=True)
    check_in_guests.short_description = "Заселить выбранных пользователей"

    def check_out_guests(self, request, queryset):
        queryset.update(is_checked_out=True)
    check_out_guests.short_description = "Выселить выбранных пользователей"


admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review)
