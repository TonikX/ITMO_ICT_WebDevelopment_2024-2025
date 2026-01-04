from django.contrib import admin
from .models import Hotel, Room, Amenity, Booking, Review, Profile

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address')
    search_fields = ('name', 'address')
    list_filter = ('owner',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'number', 'room_type', 'price')
    list_filter = ('hotel', 'room_type')
    search_fields = ('name', 'hotel__name')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'room__hotel')
    actions = ['check_in_users', 'check_out_users']

    def check_in_users(self, request, queryset):
        queryset.update(status='checked_in')
    check_in_users.short_description = "Mark selected bookings as checked in"

    def check_out_users(self, request, queryset):
        queryset.update(status='checked_out')
    check_out_users.short_description = "Mark selected bookings as checked out"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'rating', 'created_at')
