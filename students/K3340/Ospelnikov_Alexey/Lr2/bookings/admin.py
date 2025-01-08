from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'check_in_date', 'check_out_date', 'is_active']
    list_filter = ['is_active', 'check_in_date', 'check_out_date']
    search_fields = ['user__username', 'room__room_type__name', 'room__hotel__name']
    actions = ['check_in_user', 'check_out_user']

    def check_in_user(self, request, queryset):
        queryset.update(is_active=True)

    check_in_user.short_description = "Заселить пользователя"

    def check_out_user(self, request, queryset):
        queryset.update(is_active=False)

    check_out_user.short_description = "Выселить пользователя"


admin.site.register(Booking, BookingAdmin)