from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import CustomUserCreationForm, ReservationForm, ReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tour, Reservation
from django.contrib.auth.decorators import user_passes_test


class TourListView(ListView):
    model = Tour
    template_name = 'tour_list.html'
    context_object_name = 'tours'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Tour.objects.all()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(agency__name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    user_reservation = None
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(tour=tour, user=request.user).first()

    return render(request, 'tour_detail.html', {
        'tour': tour,
        'user_reservation': user_reservation,
    })


@login_required
def reserve_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    existing_reservation = Reservation.objects.filter(tour=tour, user=request.user).first()

    if existing_reservation:
        return redirect('edit_reservation', pk=existing_reservation.pk)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.tour = tour
            reservation.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = ReservationForm()

    return render(request, 'reserve_tour.html', {'form': form, 'tour': tour})


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=reservation.tour.pk)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'edit_reservation.html', {'form': form, 'reservation': reservation})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('tour_list')
    return render(request, 'delete_reservation.html', {'reservation': reservation})


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', pk=tour.pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'tour': tour})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('tour_list')


@user_passes_test(lambda user: user.is_superuser)
def sold_tours_by_country(request):
    sold_tours = (
        Tour.objects.filter(reservations__is_confirmed=True)
        .values('country', 'title', 'agency__name')
        .annotate(reservations_count=Count('reservations'))
        .order_by('country')
    )
    return render(request, 'sold_tours.html', {'sold_tours': sold_tours})
