from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking
from hotels.models import Room  # импорт модели Room из приложения hotels
from .forms import BookingForm

class RoomDetailView(DetailView):
    model = Room
    template_name = 'bookings/room_detail.html'
    context_object_name = 'room'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room_id = self.kwargs['room_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bookings:user_bookings')

class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/user_booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:user_bookings')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:user_bookings')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)