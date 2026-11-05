from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch, Q, Avg
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, CreateView, TemplateView

from reviews.models import Review
from .forms import TourForm, DepartureForm
from .models import Tour, Departure, Reservation, Country


# Create your views here.
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class TourListView(LoginRequiredMixin, ListView):
    model = Tour
    template_name = 'available_tours.html'
    paginate_by = 3

    def get_queryset(self):
        today = date.today()
        available_deps = (Departure.objects
                          .filter(start_date__gt=today)
                          .exclude(reservation__user=self.request.user)
                          .order_by('start_date'))

        queryset = (Tour.objects
                    .filter(departure__in=available_deps)
                    .prefetch_related(Prefetch('departure_set', queryset=available_deps), 'countries')
                    .order_by('title'))

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['countries'] = Country.objects.all()
        return ctx


class StaffTourListView(StaffRequiredMixin, ListView):
    model = Tour
    template_name = 'all_tours.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = (Tour.objects
                    .prefetch_related('departure_set', 'countries')
                    .order_by('title'))

        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['countries'] = Country.objects.all()
        return ctx


class TourDetailView(LoginRequiredMixin, DetailView):
    model = Tour
    template_name = 'tour.html'
    context_object_name = 'tour'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()

        if self.request.user.is_staff:
            departures = self.object.departure_set.all().order_by('start_date')
            if 'departure_form' not in ctx:
                ctx['departure_form'] = DepartureForm()
        else:
            departures = (self.object.departure_set
                          .filter(start_date__gt=today)
                          .exclude(reservation__user=self.request.user)
                          .order_by('start_date'))

        ctx['upcoming_departures'] = departures

        reviews = (Review.objects
                   .filter(departure__tour=self.object)
                   .select_related('author', 'departure')
                   .order_by('-created_at'))
        ctx['reviews'] = reviews

        ctx['avg_rating'] = reviews.aggregate(Avg('rating'))['rating__avg']

        return ctx

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('tours:detail', pk=self.get_object().pk)

        self.object = self.get_object()
        form = DepartureForm(request.POST)

        if form.is_valid():
            departure = form.save(commit=False)
            departure.tour = self.object
            departure.save()
            return redirect('tours:detail', pk=self.object.pk)

        context = self.get_context_data(departure_form=form)
        return self.render_to_response(context)


class StaffDepartureListView(StaffRequiredMixin, ListView):
    model = Departure
    template_name = 'departures.html'

    def get_queryset(self):
       queryset = (Departure.objects
                  .select_related('tour')
                  .prefetch_related('reservation_set')
                  .order_by('-start_date'))

       search = self.request.GET.get('search')

       if search:
           queryset = queryset.filter(Q(tour__title__icontains=search) | Q(tour__description__icontains=search))

       return queryset.distinct()


class StaffDepartureDetailView(StaffRequiredMixin, DetailView):
    model = Departure
    template_name = 'departure.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['reservations'] = (self.object.reservation_set
                               .select_related('user')
                               .order_by('-created_at'))
        ctx['status_choices'] = Reservation.Status.choices
        return ctx

    def post(self, request, *args, **kwargs):
        departure = self.get_object()
        reservation_id = request.POST.get('reservation_id')
        new_status = request.POST.get('status')

        if reservation_id and new_status:
            reservation = get_object_or_404(Reservation, id=reservation_id, departure=departure)
            reservation.status = new_status
            reservation.save()

        return redirect('tours:departure', pk=departure.pk)


class StaffTourCreateView(StaffRequiredMixin, CreateView):
    model = Tour
    form_class = TourForm
    template_name = 'tour_create.html'
    success_url = reverse_lazy('tours:all')


class ClientUpcomingTripsView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'upcoming_list.html'

    def get_queryset(self):
        today = date.today()
        return (Reservation.objects
                .filter(user=self.request.user, departure__end_date__gte=today)
                .select_related('departure__tour')
                .order_by('departure__start_date'))


class ReserveDepartureView(LoginRequiredMixin, View):
    def post(self, request, pk):
        departure = get_object_or_404(Departure, pk=pk)

        Reservation.objects.get_or_create(
            user=request.user,
            departure=departure,
            defaults={'status': Reservation.Status.PENDING}
        )

        return redirect('tours:upcoming')


class CancelReservationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        reservation.delete()
        return redirect('tours:upcoming')


class ClientHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        user = self.request.user

        completed_reservations = (Reservation.objects
                                  .filter(user=user, departure__end_date__lt=today)
                                  .exclude(status=Reservation.Status.REJECTED)
                                  .select_related('departure__tour')
                                  .prefetch_related('departure__tour__countries')
                                  .order_by('-departure__end_date'))


        user_reviews = Review.objects.filter(author=user)
        user_reviewed_departure_ids = set(user_reviews.values_list('departure_id', flat=True))

        ctx['completed_reservations'] = completed_reservations
        ctx['user_reviewed_departure_ids'] = user_reviewed_departure_ids

        return ctx


