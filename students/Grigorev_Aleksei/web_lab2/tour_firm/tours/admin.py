from django.contrib import admin
from .models import Tour, Reservation, Review

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'period')
    search_fields = ('name', 'agency')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'reserved_on', 'is_confirmed')
    list_filter = ('is_confirmed', 'reserved_on')
    search_fields = ('tour__name', 'user__username')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('tour__name', 'user__username')
