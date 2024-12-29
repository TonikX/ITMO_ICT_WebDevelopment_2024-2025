from django.contrib import admin
from .models import Tour, Booking, Review, Agency, Country

class BookingAdmin(admin.ModelAdmin):
    list_display = ['tour', 'user', 'is_confirmed']
    list_filter = ['is_confirmed']
    actions = ['confirm_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(is_confirmed=True)
    confirm_bookings.short_description = "Подтвердить выбранные бронирования"

class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency', 'country']
    list_filter = ['country']
    search_fields = ['name', 'agency__name']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')


admin.site.register(Tour, TourAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review)
admin.site.register(Country, CountryAdmin)