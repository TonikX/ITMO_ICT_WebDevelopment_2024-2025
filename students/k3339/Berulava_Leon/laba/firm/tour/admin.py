from django.contrib import admin
from .models import Booking

# Register your models here.

from tour.models import Tour, Review, Basket
admin.site.register(Tour)
admin.site.register(Review)
admin.site.register(Basket)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'quantity', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_bookings']

    @admin.action(description='Подтвердить выбранные бронирования')
    def approve_bookings(self, request, queryset):
        queryset.update(is_approved=True)
