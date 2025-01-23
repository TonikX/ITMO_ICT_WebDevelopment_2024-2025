from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, DetailView
from .models import Booking
from .forms import CustomUserCreationForm, BookingForm, ReviewForm, TourSearchForm, TariffFormSet, MealOptionFormSet
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import TourForm
from .models import Tour


def admin_required(function):
    return user_passes_test(lambda user: user.is_superuser)(function)


# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Вход в систему
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tour_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Выход из системы
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Список туров
def tour_list(request):
    form = TourSearchForm(request.GET)
    tours = Tour.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # Используем Q для поиска по нескольким полям
            tours = tours.filter(
                Q(hotel__icontains=query) |
                Q(country__icontains=query) |
                Q(city__icontains=query) |
                Q(description__icontains=query)
            )

    paginator = Paginator(tours, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tour_list.html', {'page_obj': page_obj, 'form': form})


# Детали тура
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    nights = (tour.end_date - tour.start_date).days
    return render(request, 'tour_detail.html', {'tour': tour, 'nights': nights})


# Резервирование тура
@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, tour=tour)
        print(form.is_valid())
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour
            booking.user = request.user
            booking.save()
            print(booking)
            return redirect('my_bookings')
    else:
        form = BookingForm(tour=tour)
    return render(request, 'book_tour.html', {'form': form, 'tour': tour})


# Обновление бронирования
class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'update_booking.html'
    success_url = reverse_lazy('my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tour'] = self.object.tour
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Booking'
        context['total_price'] = self.object.total_price
        return context


# Удаление бронирования
class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'delete_booking.html'
    success_url = reverse_lazy('my_bookings')
    title = 'Booking Cancellation'


# Детали бронирования
class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking_detail.html'
    context_object_name = 'booking'


# Мои бронирования
@login_required
def my_bookings(request):
    bookings = request.user.bookings.all()
    return render(request, 'my_bookings.html', {'bookings': bookings})


# Отзывы
@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if not request.user.bookings.filter(tour=tour, is_confirmed=True).exists():
        return redirect('my_bookings', pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'tour': tour})


# Добавление тура
@admin_required
def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)

        if form.is_valid():
            # Сохранение тура перед обработкой формсетов
            tour = form.save(commit=False)
            tour.save()

            # Привязываем сохранённый тур к формсетам
            tariff_formset = TariffFormSet(request.POST, instance=tour)
            meal_option_formset = MealOptionFormSet(request.POST, instance=tour)

            if tariff_formset.is_valid() and meal_option_formset.is_valid():
                tariff_formset.save()
                meal_option_formset.save()
                return redirect('tour_list')
        else:
            # Создание пустых формсетов при ошибке в основной форме
            tariff_formset = TariffFormSet(instance=form.instance)
            meal_option_formset = MealOptionFormSet(instance=form.instance)
    else:
        # Инициализация пустых форм
        form = TourForm()
        tariff_formset = TariffFormSet(instance=Tour())
        meal_option_formset = MealOptionFormSet(instance=Tour())

    return render(request, 'add_tour.html', {
        'form': form,
        'tariff_formset': tariff_formset,
        'meal_option_formset': meal_option_formset,
    })


# Редактирование тура
@admin_required
def edit_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        tariff_formset = TariffFormSet(request.POST, instance=tour)
        meal_option_formset = MealOptionFormSet(request.POST, instance=tour)

        if form.is_valid() and tariff_formset.is_valid() and meal_option_formset.is_valid():
            # Сохраняем изменения в туре
            form.save()

            for tariff in tariff_formset.save(commit=False):
                tariff.tour = tour
                tariff.save()

            # Удаляем только помеченные для удаления тарифы
            for tariff in tariff_formset.deleted_objects:
                tariff.delete()

            for meal_option in meal_option_formset.save(commit=False):
                meal_option.tour = tour
                meal_option.save()

            # Удаляем только помеченные для удаления варианты питания
            for meal_option in meal_option_formset.deleted_objects:
                meal_option.delete()

            return redirect('tour_list')

    else:
        form = TourForm(instance=tour)
        tariff_formset = TariffFormSet(instance=tour)
        meal_option_formset = MealOptionFormSet(instance=tour)

    return render(request, 'edit_tour.html', {
        'form': form,
        'tariff_formset': tariff_formset,
        'meal_option_formset': meal_option_formset,
    })


# Просмотр бронирований администратором
@admin_required
def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})


# Подтверждение бронирований пользователей
@admin_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_confirmed = True
    booking.save()
    return redirect('view_bookings')


# Проданные туры по странам
@admin_required
def sold_tours_by_country(request):
    tours_by_country = (
        Tour.objects.filter(bookings__is_confirmed=True)
        .values('country')
        .annotate(total_bookings=Count('bookings'))
        .order_by('-total_bookings')
    )
    return render(request, 'sold_tours.html', {'tours_by_country': tours_by_country})
