from django.contrib import admin
from .models import Hotel, Room, Booking, Review


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address')
    search_fields = ('name', 'owner', 'address')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'price', 'capacity')
    list_filter = ('room_type', 'hotel')
    search_fields = ('hotel__name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date_from', 'date_to', 'status')
    list_filter = ('status', 'date_from', 'date_to')
    search_fields = ('user__username',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'rating', 'stay_from', 'stay_to')
    list_filter = ('rating',)
    search_fields = ('user__username',)
