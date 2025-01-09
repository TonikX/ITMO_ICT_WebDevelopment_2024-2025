from django.contrib import admin
from django.utils.html import format_html

from hotel_list.models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner')
    search_fields = ('name', 'address')
    list_filter = ('owner',)
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'n_people', 'cost', 'room_type')
    search_fields = ('hotel__name', 'room_type__room_type', 'cost')
    list_filter = ('hotel', 'room_type', 'n_people')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "hotel":
            kwargs["queryset"] = Hotel.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'room',
        'hotel_name',
        'status',
        'stay_period',
        'projected_income',
        'dt_start',
        'dt_end'
    )
    search_fields = ('user__username', 'room__hotel__name', 'room__hotel__address', 'status')
    list_filter = ('status', 'room__hotel', 'dt_start', 'dt_end')
    date_hierarchy = 'dt_start'
    ordering = ('-dt_start',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(room__hotel__owner=request.user)

    def hotel_name(self, obj):
        return obj.room.hotel.name

    hotel_name.short_description = "Hotel Name"

    def stay_period(self, obj):
        return (obj.dt_end - obj.dt_start).days

    stay_period.short_description = "Stay Period (nights)"

    def projected_income(self, obj):
        stay_length = (obj.dt_end - obj.dt_start).days
        projected_income = obj.room.cost * stay_length
        return f"${projected_income}"

    projected_income.short_description = "Projected Income"

    actions = ['approve_reservations', 'cancel_reservations']

    def approve_reservations(self, request, queryset):
        queryset.update(status='ap')
        self.message_user(request, f"{queryset.count()} reservation(s) approved.")

    approve_reservations.short_description = "Approve selected reservations"

    def cancel_reservations(self, request, queryset):
        queryset.update(status='ca')
        self.message_user(request, f"{queryset.count()} reservation(s) canceled.")

    cancel_reservations.short_description = "Cancel selected reservations"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservation_info', 'hotel_name', 'author', 'rating', 'text', 'created_date')
    search_fields = ('reservation__room__hotel__name', 'author__username', 'text')
    list_filter = ('reservation__room__hotel', 'rating')
    ordering = ('-reservation__dt_start', '-rating',)
    readonly_fields = ('reservation', 'author', 'text', 'rating')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reservation__room__hotel__owner=request.user)

    def reservation_info(self, obj):
        return f"Room {obj.reservation.room.id} ({obj.reservation.dt_start} - {obj.reservation.dt_end})"

    reservation_info.short_description = "Reservation Details"

    def hotel_name(self, obj):
        return obj.reservation.room.hotel.name

    hotel_name.short_description = "Hotel"

    def created_date(self, obj):
        return obj.reservation.dt_start

    created_date.short_description = "Review Date"

    def rating(self, obj):
        if obj.rating <= 3:
            return format_html('<span style="color: red;">{}</span>', obj.rating)
        return obj.rating

    rating.short_description = "Rating"


# Register your models here.
admin.site.register(RoomType)
admin.site.register(Convenience)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Review, ReviewAdmin)
