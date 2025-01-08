from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room
from bookings.forms import BookingForm
from reviews.forms import ReviewForm


def hotel_list(request):
    hotels_list = Hotel.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(hotels_list, 5)  # 5 объектов на страницу
    hotels = paginator.page(page)
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})
def home(request):
    return render(request, 'hotels/home.html')

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = hotel.rooms.all()
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    reviews = room.reviews.all()
    booking_form = BookingForm()
    review_form = ReviewForm()
    if request.method == "POST":
        if 'booking_submit' in request.POST:
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.save()
                booking_form = BookingForm()
        elif 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                review_form = ReviewForm()

    return render(request, 'hotels/room_detail.html',
                  {'room': room, 'reviews': reviews, 'booking_form': booking_form, 'review_form': review_form})