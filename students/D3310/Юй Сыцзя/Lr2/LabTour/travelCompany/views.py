from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from travelCompany.forms import UserRegistrationForm, UserLoginForm, TourForm, CreateAgency, CreateTour
from travelCompany.models import Tour, TravelAgency, Reservation, Review, SoldTour
from .forms import ReviewForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('tour_firm_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def tour_firm_list(request):
    query = request.GET.get('q')
    agency = TravelAgency.objects.all()

    if query:
        agency = agency.filter(name__icontains=query)

    paginator = Paginator(agency, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tour/tour_firm_list.html', {'page_obj': page_obj, 'query': query})


@login_required
def tour_list(request, tour_id):
    tour_firm = get_object_or_404(TravelAgency, id=tour_id)
    tours = Tour.objects.filter(agency=tour_firm).order_by('id')
    paginator = Paginator(tours, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tour/tour_list.html', {'tour_firm': tour_firm, 'page_obj': page_obj})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    user_has_reserved = Reservation.objects.filter(user=request.user,
                                                   tour=tour).exists() if request.user.is_authenticated else False

    # Initialize reservation as None
    reservation = None
    if user_has_reserved:
        reservation = Reservation.objects.get(user=request.user, tour=tour)

    return render(request, 'tour/tour_detail.html', {
        'tour': tour,
        'user_has_reserved': user_has_reserved,
        'reservation': reservation,
    })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


@login_required
def tour_reviews(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour).order_by('-date')
    return render(request, 'tour/tour_reviews.html', {'tour': tour, 'reviews': reviews})


@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    # Check if the user already has a reservation for the tour
    if Reservation.objects.filter(user=request.user, tour=tour).exists():
        return HttpResponse("Вы уже забронировали этот тур.")

    # Create a new reservation
    Reservation.objects.create(user=request.user, tour=tour)

    # Send a success message
    return render(request, 'tour/tour_detail.html', {
        'tour': tour,
        'user_has_reserved': True,
        'message': 'Тур успешно забронирован!'
    })


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/my_reservations.html', {'reservations': reservations})


def add_review(request, tour_id):
    tour = Tour.objects.get(id=tour_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()

            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()

    return render(request, 'reservation/add_review.html', {'form': form, 'tour': tour})


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('tour_detail', tour_id=reservation.tour.id)


class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    template_name = 'tour/tour_update.html'
    context_object_name = 'tour'
    pk_url_kwarg = 'tour_id'

    def get_success_url(self):
        return reverse_lazy('tour_detail', kwargs={'tour_id': self.object.id})

    def get_object(self, queryset=None):
        return get_object_or_404(Tour, id=self.kwargs['tour_id'])


@login_required
def sold_tours_by_country(request):
    sold_tours = SoldTour.objects.all()
    tours_by_country = {}

    for sold_tour in sold_tours:
        country = sold_tour.tour.country
        if country not in tours_by_country:
            tours_by_country[country] = []
        tours_by_country[country].append(sold_tour)

    return render(request, 'tour/sold_tours_by_country.html', {'tours_by_country': tours_by_country})


@login_required
@staff_member_required
def all_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservation/all_reservations.html', {'reservations': reservations})


@login_required
@staff_member_required
def reservation_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    tour_id = reservation.tour.id
    reservation.delete()
    return redirect('all_reservations')


@login_required
@staff_member_required
def add_agency(request):
    if request.method == 'POST':
        form = CreateAgency(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)

            tour.agency = TravelAgency.objects.first()
            tour.save()
            return redirect('tour_firm_list')
    else:
        form = CreateAgency()

    return render(request, 'tour/add_tour.html', {'form': form})


@login_required
@staff_member_required
def add_tour(request):
    if request.method == 'POST':
        form = CreateTour(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.agency = TravelAgency.objects.first()
            tour.save()
            return redirect('tour_firm_list')
    else:
        form = CreateTour()

    return render(request, 'tour/add_new_tour.html', {'form': form})


@login_required
@staff_member_required
def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tour_firm_list')


def home(request):
    return render(request, 'main.html')

