from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import login, logout
from .models import Tour, Reservation, Review, User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservationForm, ReviewForm, CustomUserCreationForm


class HomeView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        tours = Tour.objects.all()
        user = request.user
        return render(request, 'home.html', {
            'form': form,
            'tours': tours,
            'user': user
        })

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
        return render(request, 'home.html', {
            'form': form,
            'tours': Tour.objects.all(),
        })


class AdminApproveReservationView(View):
    def post(self, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)

        if not reservation.is_confirmed:
            reservation.is_confirmed = True
            reservation.save()

            country_sales = reservation.tour.country
            if country_sales:
                country_sales.total_sales += 1
                country_sales.save()

        return redirect('admin_reservations')


class UserCancelReservationView(View):
    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        reservation.delete()
        return redirect('user_reservations')


class AdminReservationsView(View):
    def get(self, request):
        reservations = Reservation.objects.select_related('user', 'tour').all()
        return render(request, 'admin_reservations.html', {'reservations': reservations})



class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class UserRegistrationView(View):
    form_class = CustomUserCreationForm
    template_name = 'user_register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class TourListView(ListView):
    model = Tour
    template_name = 'tour_list.html'
    context_object_name = 'tours'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        title_query = self.request.GET.get('title', '')
        agency_query = self.request.GET.get('agency', '')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if agency_query:
            queryset = queryset.filter(agency__icontains=agency_query)

        if start_date and end_date:
            queryset = queryset.filter(
                Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
            )
        elif start_date:
            queryset = queryset.filter(end_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(start_date__lte=end_date)

        print(f"Фильтрованный результат содержит {queryset.count()} туров.")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()

        query_params.pop('page', None)

        context['last_question'] = query_params.urlencode()
        print(f"Контекст пагинации: {context.get('paginator')}, Текущая страница: {context.get('page_obj')}")
        print(f"Параметры запроса для пагинации: {context['last_question']}")

        return context


class TourDetailView(View):
    def get(self, request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        return render(request, 'tour_detail.html', {'tour': tour})


class TourDetailView(View):
    def get(self, request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        similar_tours = Tour.objects.filter(title=tour.title)
        reviews = Review.objects.filter(tour__in=similar_tours)
        review_form = ReviewForm()

        return render(request, 'tour_detail.html', {
            'tour': tour,
            'reviews': reviews,
            'review_form': review_form,
        })


class CancelReservationView(View):
    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        reservation.delete()

        return redirect('user_reservations')


class ConfirmedToursByCountryView(View):
    def get(self, request):
        confirmed_reservations = Reservation.objects.filter(is_confirmed=True).select_related('tour__country')

        countries = {}
        for reservation in confirmed_reservations:
            country_sales = reservation.tour.country
            country_name = country_sales.country

            if country_name not in countries:
                countries[country_name] = []
            countries[country_name].append(reservation.tour)

        return render(request, 'confirmed_tours_by_country.html', {'countries': countries})


class UserConfirmedToursByCountryView(View):
    def get(self, request):
        confirmed_reservations = Reservation.objects.filter(
            is_confirmed=True, user=request.user
        ).select_related('tour__country')

        countries = {}
        for reservation in confirmed_reservations:
            country_sales = reservation.tour.country
            country_name = country_sales.country

            if country_name not in countries:
                countries[country_name] = []
            countries[country_name].append(reservation.tour)

        return render(request, 'user_confirmed_tours_by_country.html', {'countries': countries})


class ReservationCreateView(View):
    def get(self, request, tour_id, user_id):
        form = ReservationForm()
        user = get_object_or_404(User, id=user_id)
        tour = get_object_or_404(Tour, id=tour_id)
        return render(request, 'reserve_tour.html', {'form': form, 'tour': tour, 'user': user})

    def post(self, request, tour_id, user_id):
        form = ReservationForm(request.POST)
        tour = get_object_or_404(Tour, id=tour_id)
        user = get_object_or_404(User, id=user_id)

        if Reservation.objects.filter(user=user, tour=tour).exists():
            messages.warning(request, "Вы уже зарезервировали место на этот тур.")
            return redirect('tour_detail', tour_id=tour_id)

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = user
            reservation.tour = tour
            reservation.save()
            messages.success(request, "Вы успешно зарезервировали место на тур.")
            return redirect('tour_detail', tour_id=tour_id)

        return render(request, 'reserve_tour.html', {'form': form, 'tour': tour, 'user': user})


class ReviewCreateView(View):
    def post(self, request, tour_id):
        tour = get_object_or_404(Tour, id=tour_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', tour_id=tour_id)

        similar_tours = Tour.objects.filter(title=tour.title)
        reviews = Review.objects.filter(tour__in=similar_tours)

        return render(request, 'tour_detail.html', {
            'tour': tour,
            'reviews': reviews,
            'review_form': form,
        })


class UserReservationsView(View):
    def get(self, request):
        reservations = request.user.reservations.all()
        return render(request, 'user_reservations.html', {'reservations': reservations})
