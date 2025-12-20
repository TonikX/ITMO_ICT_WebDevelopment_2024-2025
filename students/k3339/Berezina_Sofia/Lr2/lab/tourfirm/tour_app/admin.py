from django.contrib import admin
from .models import Tour, Reservation, Review

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['title', 'agency', 'country', 'start_date', 'end_date', 'price']
    list_filter = ['agency', 'country', 'start_date']
    search_fields = ['title', 'description']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'reservation_date', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['user__username', 'tour__title']
    list_editable = ['status']
    actions = ['confirm_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f'{queryset.count()} резервирований подтверждено')
    confirm_reservations.short_description = "Подтвердить выбранные резервирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'tour', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'tour__title', 'text']