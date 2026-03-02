from django.shortcuts import render, get_object_or_404
from .models import Booking
from .models import Hotel, Room
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Hotel



def hotel_list(request):
    hotel_list = Hotel.objects.all()

    paginator = Paginator(hotel_list, 6)  # 6 отелей на страницу
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)

    return render(request, 'hotels/hotel_list.html', {
        'hotels': hotels
    })


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = Room.objects.filter(hotel=hotel)

    room_type = request.GET.get('type')
    max_price = request.GET.get('max_price')
    capacity = request.GET.get('capacity')

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if max_price:
        rooms = rooms.filter(price__lte=max_price)

    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)

    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import BookingForm
from .models import Room


@login_required
def create_booking(request, room_id):
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'hotels/create_booking.html', {
        'form': form,
        'room': room
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})


from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'hotels/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')

@staff_member_required
def last_month_guests(request):
    month_ago = timezone.now().date() - timedelta(days=30)

    bookings = Booking.objects.filter(
        date_from__gte=month_ago,
        status__in=['checked_in', 'checked_out']
    ).select_related('user', 'room', 'room__hotel')

    return render(request, 'hotels/last_month_guests.html', {
        'bookings': bookings
    })

from django.contrib.admin.views.decorators import staff_member_required
from .models import Booking

@staff_member_required
def admin_bookings(request):
    bookings = Booking.objects.select_related("user", "room", "room__hotel")
    return render(request, "hotels/admin_bookings.html", {
        "bookings": bookings
    })


