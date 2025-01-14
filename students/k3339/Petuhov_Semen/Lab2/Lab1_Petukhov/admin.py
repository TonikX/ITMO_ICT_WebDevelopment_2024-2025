from django.contrib import admin
from .models import Tour, Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'reservation_date', 'is_confirmed', 'payment_conditions')
    list_filter = ('is_confirmed', 'reservation_date')
    search_fields = ('user__username', 'tour__name')
    actions = ['confirm_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(is_confirmed=True)
    confirm_reservations.short_description = "Подтвердить выбранные бронирования"


admin.site.register(Tour)
admin.site.register(Reservation, ReservationAdmin)