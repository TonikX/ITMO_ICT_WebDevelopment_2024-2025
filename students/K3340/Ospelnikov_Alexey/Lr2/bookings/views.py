from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'bookings/booking_delete.html', {'booking': booking})

@login_required
def current_guests(request):
    today = timezone.now().date()
    last_month = today.replace(day=1) - timezone.timedelta(days=1)
    last_month = last_month.replace(day=1)
    bookings = Booking.objects.filter(check_in_date__lte=today, check_out_date__gte=last_month)
    return render(request, 'bookings/guests.html', {'bookings': bookings})