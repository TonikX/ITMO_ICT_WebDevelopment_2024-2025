from django.contrib import admin
from .models import Hotel, Room, RoomType, Reservation, Review, Owner


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner')
    search_fields = ('name', 'address')
    list_filter = ('owner',)


admin.site.register(Hotel, HotelAdmin)


class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity')
    search_fields = ('name',)


admin.site.register(RoomType, RoomTypeAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'room_price', 'room_capacity')

    def room_price(self, obj):
        return obj.room_type.price

    def room_capacity(self, obj):
        return obj.room_type.capacity

    room_price.short_description = 'Price'
    room_capacity.short_description = 'Capacity'

    search_fields = ('hotel__name', 'room_type')
    list_filter = ('hotel', 'room_type')


admin.site.register(Room, RoomAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'room_type', 'stay_period', 'rating')
    search_fields = ('user__username', 'room_type__name', 'comment')
    list_filter = ('rating',)


admin.site.register(Review, ReviewAdmin)


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Reservation)

admin.site.register(Owner, OwnerAdmin)
