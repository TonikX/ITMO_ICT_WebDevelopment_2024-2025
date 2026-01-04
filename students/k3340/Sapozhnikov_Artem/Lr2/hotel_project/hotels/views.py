from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Hotel, Room, Booking
from .forms import BookingForm, ReviewForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 10

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = self.object.rooms.all()
        return context
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotels:hotel_list')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def hotel_detail(request, hotel_id):
    hotel = Hotel.objects.get(pk=hotel_id)

    # Показываем только свободные номера:
    rooms = Room.objects.filter(hotel=hotel).exclude(
        bookings__check_out__gte=date.today(),
        bookings__status__in=['reserved', 'checked_in']
    ).distinct()

    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

@login_required
def booking_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    active_bookings = room.bookings.filter(check_out__gte=date.today(), status__in=['reserved', 'checked_in'])
    if active_bookings.exists():
        messages.error(request, "Этот номер уже забронирован.")
        if room.hotel_id:
            return redirect('hotels:hotel_detail', hotel_id=room.hotel_id)
        return redirect('hotels:hotel_list')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.status = 'reserved'
            booking.save()
            messages.success(request, "Бронирование успешно создано!")
            if room.hotel_id:
                return redirect('hotels:hotel_detail', hotel_id=room.hotel_id)
            return redirect('hotels:hotel_list')
    else:
        form = BookingForm()

    return render(request, 'hotels/booking_form.html', {'form': form, 'room': room})

@login_required
def room_review(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.select_related('user').all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Спасибо за ваш отзыв!")
            return redirect('hotels:room_review', room_id=room.id)
    else:
        form = ReviewForm()

    return render(request, 'hotels/room_review.html', {
        'room': room,
        'form': form,
        'reviews': reviews
    })

class RoomDetailView(DetailView):
    model = Room
    template_name = 'hotels/room_detail.html'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotels/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'room': self.get_room()}
        return kwargs

    def get_room(self):
        from .models import Room
        return Room.objects.get(pk=self.kwargs['room_id'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room = self.get_room()
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('hotels:user_bookings')


class UserBookingsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotels/user_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class RecentGuestsListView(ListView):
    model = Booking
    template_name = 'hotels/recent_guests.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        since = date.today() - timedelta(days=30)
        return Booking.objects.filter(check_out__gte=since, check_in__lte=date.today()).select_related('user', 'room')

# class BookingEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Booking
#     form_class = BookingForm
#     template_name = 'hotels/booking_form.html'
#
#     def test_func(self):
#         booking = self.get_object()
#         return booking.user == self.request.user  # Только владелец может редактировать
#
#     def form_valid(self, form):
#         messages.success(self.request, "Бронирование обновлено!")
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('hotels:user_bookings')


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.delete()
    messages.success(request, "Бронирование успешно удалено.")
    return redirect('hotels:user_bookings')

@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование успешно обновлено.")
            return redirect('hotels:user_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'hotels/booking_edit_form.html', {'form': form, 'booking': booking})
