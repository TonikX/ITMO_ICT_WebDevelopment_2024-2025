from django.contrib import admin
from .models import Amenity, Hotel, RoomType, Room, Reservation, Review


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'get_rooms_count', 'get_active_rooms')
    search_fields = ('name', 'address', 'owner__username')
    inlines = [RoomInline]

    def get_rooms_count(self, obj):
        return obj.rooms.count()
    get_rooms_count.short_description = 'Всего номеров'

    def get_active_rooms(self, obj):
        active = obj.rooms.filter(is_active=True).count()
        total = obj.rooms.count()
        return f"{active} из {total}"
    get_active_rooms.short_description = 'Доступно номеров'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'room_type', 'price_per_night', 'capacity', 'is_active')
    list_filter = ('hotel', 'room_type', 'is_active', 'amenities')
    search_fields = ('hotel__name', 'room_type__name')
    autocomplete_fields = ['hotel', 'room_type', 'amenities']
    list_editable = ['is_active', 'price_per_night']


@admin.action(description='Заселить выбранные бронирования')
def mark_checked_in(modeladmin, request, queryset):
    queryset.update(status=Reservation.Status.CHECKED_IN)


@admin.action(description='Выселить выбранные бронирования')
def mark_checked_out(modeladmin, request, queryset):
    queryset.update(status=Reservation.Status.CHECKED_OUT)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('user__username', 'room__hotel__name')
    autocomplete_fields = ['user', 'room']
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'check_in'
    actions = [mark_checked_in, mark_checked_out]
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status=Reservation.Status.CONFIRMED)
    mark_as_confirmed.short_description = "Подтвердить выбранные бронирования"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'room__hotel')
    search_fields = ('user__username', 'room__hotel__name', 'text')
    autocomplete_fields = ['user', 'room']
    readonly_fields = ('created_at',)