from django.contrib import admin, messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, TicketNumberForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from django.urls import path, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'seat', 'first_name', 'last_name')
    actions = ['register_passenger_to_flight']

    def register_passenger_to_flight(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        return HttpResponseRedirect(
            reverse("admin:register_passenger") + f"?reservations={','.join(map(str, selected))}")
    register_passenger_to_flight.short_description = "Register passenger to a flight with ticket number"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('flights_app/reservation/register_passenger/',
                 self.admin_site.admin_view(self.register_passenger_view), name="register_passenger"),
        ]
        return custom_urls + urls

    def register_passenger_view(self, request):
        reservation_ids = request.GET.get('reservations')
        if not reservation_ids:
            self.message_user(request, "No reservations selected.", messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        reservation_ids = reservation_ids.split(',')
        reservations = Reservation.objects.filter(pk__in=reservation_ids)

        if request.method == 'POST':
            form = TicketNumberForm(request.POST)
            if form.is_valid():
                ticket_number = form.cleaned_data['ticket_number']

                for reservation in reservations:
                    if Passenger.objects.filter(flight=reservation.flight, seat=reservation.seat).exists():
                        self.message_user(
                            request,
                            f"Passenger with seat {reservation.seat} for flight {reservation.flight} is already registered.",
                            messages.WARNING
                        )
                        continue

                    passenger = Passenger(
                        flight=reservation.flight,
                        seat=reservation.seat,
                        first_name=reservation.first_name,
                        last_name=reservation.last_name,
                        ticket_number=ticket_number
                    )
                    passenger.save()

                    self.message_user(
                        request,
                        f"Successfully registered {reservation.first_name} {reservation.last_name} with ticket number {ticket_number}.",
                        messages.SUCCESS
                    )

                return HttpResponseRedirect("/admin/flights_app/reservation/")

        else:
            form = TicketNumberForm()

        return render(request, 'admin/register_passenger.html',
                      {'form': form, 'reservations': reservations})


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Review)
admin.site.register(Passenger)
