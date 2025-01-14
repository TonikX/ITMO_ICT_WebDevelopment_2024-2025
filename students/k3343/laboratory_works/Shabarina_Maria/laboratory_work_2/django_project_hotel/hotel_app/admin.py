from django.contrib import admin
from .models import Hotel, Room, RoomType, Review, Reservation, CustomUser
from django.utils import timezone


class LastMonthFilter(admin.SimpleListFilter):
    title = 'Data'
    parameter_name = 'last_month_reservations'

    def lookups(self, request, model_admin):
        return [('last_month_reservations', 'Last month reservations')]

    def queryset(self, request, queryset):
        if self.value() == 'last_month':
            return queryset.filter(start_date__gte=timezone.now() - timezone.timedelta(days=30))
        return queryset


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'start_date', 'end_date', 'status')
    actions = ['check_in', 'check_out']
    list_filter = (LastMonthFilter,)

    def check_in(self, request, queryset):
        queryset.update(status='checked_in')

    def check_out(self, request, queryset):
        queryset.update(status='checked_out')


admin.site.register(Hotel)
admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Review)
admin.site.register(Reservation, ReservationAdmin)
