from django.contrib import admin
from .models import Hotel, Room, RoomType, Booking, Review, Guest

# Админ-панель отеля
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address')
    search_fields = ('name', 'address')
    list_filter = ('owner',)

# Админ-панель типа комнаты
@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Админ-панель номера отеля
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'cost_per_night', 'capacity')
    list_filter = ('hotel', 'room_type', 'capacity')
    search_fields = ('hotel__name', 'room_type__name')

# Админ-панель бронирования
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'room__hotel__name')

    actions = ['mark_as_checked_in', 'mark_as_checked_out']

    def mark_as_checked_in(self, request, queryset):
        updated = queryset.update(status='checked_in')
        self.message_user(request, f"{updated} booking(s) marked as Checked In.")

    def mark_as_checked_out(self, request, queryset):
        updated = queryset.update(status='checked_out')
        self.message_user(request, f"{updated} booking(s) marked as Checked Out.")

    mark_as_checked_in.short_description = 'Mark selected bookings as Checked In'
    mark_as_checked_out.short_description = 'Mark selected bookings as Checked Out'

# Админ-панель отзывов
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'get_start_date', 'get_end_date')
    list_filter = ('rating',)
    search_fields = ('booking__user__username', 'comment')

    def get_start_date(self, obj):
        return obj.booking.start_date
    get_start_date.short_description = 'Start Date'

    def get_end_date(self, obj):
        return obj.booking.end_date
    get_end_date.short_description = 'End Date'

# Админ-панель гостей
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'is_primary_guest')
    list_filter = ('is_primary_guest',)
    search_fields = ('user__username',)