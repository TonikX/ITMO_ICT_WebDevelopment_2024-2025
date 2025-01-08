from django.contrib import admin
from .models import *


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    readonly_fields = ('arrival_date',)
    list_display = ('number', 'departure_date', 'arrival_date', 'route', 'status')

    def save_model(self, request, obj, form, change):
        if obj.departure_date and obj.route:
            obj.arrival_date = obj.departure_date + timedelta(days=obj.route.arrival_day or 0)
        super().save_model(request, obj, form, change)


def sell_selected_seats(modeladmin, request, queryset):

    for seat in queryset:
        if not seat.is_sold:
            seat.is_sold = True
            seat.save()

            flight = seat.flight
            flight.sold_tickets_number = flight.seats.filter(is_sold=True).count()
            flight.save()

    modeladmin.message_user(request, "Selected seats have been sold and ticket counts updated.")


class SeatAdmin(admin.ModelAdmin):
    list_display = ['number', 'flight', 'is_sold']
    actions = [sell_selected_seats]


admin.site.register(Airline)
admin.site.register(Airport)
admin.site.register(PlaneModel)
admin.site.register(Plane)
admin.site.register(Maintenance)
admin.site.register(Employee)
admin.site.register(CrewMember)
admin.site.register(Crew)
admin.site.register(Route)
admin.site.register(Seat, SeatAdmin)
admin.site.register(TransitStop)
admin.site.register(User)