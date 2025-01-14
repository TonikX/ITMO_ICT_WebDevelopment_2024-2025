from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Tour, Reservation, Comment
from django import forms
from django.contrib.auth.decorators import user_passes_test

class CommentForm(forms.Form):
    travel_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата поездки"
    )
    text = forms.CharField(
        widget=forms.Textarea,
        label="Текст комментария"
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=10,
        label="Оценка (1-10)"
    )
# Форма для выбора даты бронирования
class ReservationDateForm(forms.Form):
    reservation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Выберите дату бронирования"
    )


class EditReservationForm(forms.Form):
    reservation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата бронирования"
    )
    payment_conditions = forms.CharField(
        widget=forms.Textarea,
        label="Условия оплаты"
    )

# Проверка на администратора
def admin_required(user):
    return user.is_authenticated and user.is_staff

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour_detail.html', {'tour': tour})


@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    current_year = datetime.now().year
    start_date = datetime.strptime(f"{current_year}.{tour.start_date}", "%Y.%d.%m").date()
    end_date = datetime.strptime(f"{current_year}.{tour.end_date}", "%Y.%d.%m").date()

    if request.method == 'POST':
        form = ReservationDateForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']

            # Проверка, что дата бронирования лежит в пределах дат тура
            if start_date <= reservation_date <= end_date:
                # Создаем бронирование
                Reservation.objects.create(
                    tour=tour,
                    user=request.user,
                    reservation_date=reservation_date
                )
                return redirect('my_tours')
            else:
                form.add_error('reservation_date', 'Дата бронирования должна быть в пределах периода тура.')

    else:
        form = ReservationDateForm()

    return render(request, 'reserve_tour.html', {
        'tour': tour,
        'form': form
    })


@login_required
def my_tours(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'my_tours.html', {'reservations': reservations})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    tour = reservation.tour

    current_year = datetime.now().year
    start_date = datetime.strptime(f"{current_year}.{tour.start_date}", "%Y.%d.%m").date()
    end_date = datetime.strptime(f"{current_year}.{tour.end_date}", "%Y.%d.%m").date()

    if request.method == 'POST':
        form = EditReservationForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']
            payment_conditions = form.cleaned_data['payment_conditions']

            if start_date <= reservation_date <= end_date:
                reservation.reservation_date = reservation_date
                reservation.payment_conditions = payment_conditions
                reservation.save()
                return redirect('my_tours')
            else:
                form.add_error('reservation_date', 'Дата бронирования должна быть в пределах периода тура.')

    else:
        form = EditReservationForm(initial={
            'reservation_date': reservation.reservation_date,
            'payment_conditions': reservation.payment_conditions
        })

    return render(request, 'edit_reservation.html', {
        'form': form,
        'tour': tour,
    })


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()
    return redirect('my_tours')

@login_required
def add_comment(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                tour=tour,
                user=request.user,
                travel_date=form.cleaned_data['travel_date'],
                text=form.cleaned_data['text'],
                rating=form.cleaned_data['rating']
            )
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {
        'form': form,
        'tour': tour,
    })

@user_passes_test(admin_required)
def confirmed_tours_by_country(request):
    # Группируем подтвержденные бронирования по странам
    countries = {}
    confirmed_reservations = Reservation.objects.filter(is_confirmed=True).select_related('tour')

    for reservation in confirmed_reservations:
        country = reservation.tour.country
        if country not in countries:
            countries[country] = []
        countries[country].append(reservation)

    return render(request, 'confirmed_tours_by_country.html', {'countries': countries})
