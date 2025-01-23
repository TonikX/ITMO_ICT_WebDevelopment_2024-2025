from django.contrib import admin
from .models import Tour, TourAgency, Reservation, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency', 'start_date', 'end_date')
    search_fields = ('title', 'agency__name')

    def confirm_reservations(self, request, queryset):
        queryset.update(is_confirmed=True)

    confirm_reservations.short_description = "Confirm selected reservations"


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'is_confirmed')
    list_filter = ('is_confirmed',)
    search_fields = ('tour__title', 'user__username')


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(TourAgency)
admin.site.register(Review)
