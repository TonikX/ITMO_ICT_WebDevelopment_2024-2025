from django.contrib import admin
from .models import TourAgency, Tour, Reservation, Review

@admin.register(TourAgency)
class TourAgencyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency', 'start_date', 'end_date', 'country']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'reservation_date', 'confirmed']
    list_filter = ['confirmed']
    actions = ['confirm_reservations']

    def confirm_reservations(self, queryset):
        queryset.update(confirmed=True)
    confirm_reservations.short_description = "Подтвердить выбранные резервирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['tour', 'user', 'rating', 'review_date']