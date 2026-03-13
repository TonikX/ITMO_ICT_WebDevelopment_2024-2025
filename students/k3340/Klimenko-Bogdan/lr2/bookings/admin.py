from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'is_checked_in', 'is_checked_out')
    list_filter = ('is_checked_in', 'is_checked_out')
    search_fields = ('user__username', 'room__hotel__name')