from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Flight, Reservation, Comment
from .forms import ReservationForm, CommentForm


class FlightListView(ListView):
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'


class FlightDetailView(DetailView):
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        context['reservations'] = Reservation.objects.filter(flight=flight)
        context['comments'] = Comment.objects.filter(flight=flight).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


@login_required
def create_reservation(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            messages.success(request, 'Бронирование успешно создано.')
            return redirect('flight_detail', pk=flight.id)
    else:
        form = ReservationForm()
    return render(request, 'flights/reservation_form.html', {'form': form, 'flight': flight})


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'flights/reservation_form.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flight"] = self.object.flight  # Ensure flight is passed
        return context

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'flights/reservation_confirm_delete.html'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('flight_detail', kwargs={'pk': self.object.flight.id})


@login_required
def create_comment(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.flight = flight
            comment.user = request.user
            comment.save()
            messages.success(request, 'Отзыв успешно добавлен.')
        else:
            messages.error(request, 'Ошибка при заполнении формы отзыва.')
    return redirect('flight_detail', pk=flight.id)
