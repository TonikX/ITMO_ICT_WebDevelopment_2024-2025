from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import (
    Race, Driver, Car, Team, Comment, Registration, RaceResult, CustomUser
)
from .forms import (
    CustomUserCreationForm, DriverForm, CarForm, CommentForm,
    RegistrationForm, RaceResultForm
)


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('race_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'races/register.html', {'form': form})


def race_list(request):
    races = Race.objects.all().order_by('-date')
    search_query = request.GET.get('search', '')

    if search_query:
        races = races.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(races, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'races/race_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def race_detail(request, pk):
    race = get_object_or_404(Race, pk=pk)
    results = race.results.all().order_by('position')
    comments = race.comments.all()
    registrations = race.registrations.all()

    context = {
        'race': race,
        'results': results,
        'comments': comments,
        'registrations': registrations,
    }
    return render(request, 'races/race_detail.html', context)


@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    try:
        driver = Driver.objects.get(user=request.user)
    except Driver.DoesNotExist:
        return redirect('create_driver_profile')

    if request.method == 'POST':
        Registration.objects.get_or_create(driver=driver, race=race)
        return redirect('race_detail', pk=race.pk)

    return render(request, 'races/register_race.html', {'race': race})


@login_required
def unregister_from_race(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    driver = get_object_or_404(Driver, user=request.user)
    registration = get_object_or_404(Registration, driver=driver, race=race)
    registration.delete()
    return redirect('race_detail', pk=race.pk)


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            return redirect('race_detail', pk=race.pk)
    else:
        form = CommentForm()
    return render(request, 'races/add_comment.html', {'form': form, 'race': race})


def driver_list(request):
    drivers = Driver.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        drivers = drivers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(team__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(drivers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'races/driver_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


def driver_detail(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    car = get_object_or_404(Car, driver=driver)
    results = driver.registrations.all()

    context = {
        'driver': driver,
        'car': car,
        'results': results,
    }
    return render(request, 'races/driver_detail.html', context)


@login_required
def create_driver_profile(request):
    try:
        driver = Driver.objects.get(user=request.user)
        return redirect('driver_detail', pk=driver.pk)
    except Driver.DoesNotExist:
        pass

    if request.method == 'POST':
        driver_form = DriverForm(request.POST)
        car_form = CarForm(request.POST)

        if driver_form.is_valid() and car_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.user = request.user
            driver.save()

            car = car_form.save(commit=False)
            car.driver = driver
            car.save()

            return redirect('driver_detail', pk=driver.pk)
    else:
        driver_form = DriverForm()
        car_form = CarForm()

    return render(request, 'races/create_driver_profile.html', {
        'driver_form': driver_form,
        'car_form': car_form
    })


@login_required
def edit_driver_profile(request, pk):
    driver = get_object_or_404(Driver, pk=pk)

    if driver.user != request.user:
        return redirect('driver_detail', pk=pk)

    car = get_object_or_404(Car, driver=driver)

    if request.method == 'POST':
        driver_form = DriverForm(request.POST, instance=driver)
        car_form = CarForm(request.POST, instance=car)

        if driver_form.is_valid() and car_form.is_valid():
            driver_form.save()
            car_form.save()
            return redirect('driver_detail', pk=driver.pk)
    else:
        driver_form = DriverForm(instance=driver)
        car_form = CarForm(instance=car)

    return render(request, 'races/edit_driver_profile.html', {
        'driver_form': driver_form,
        'car_form': car_form,
        'driver': driver
    })


def race_leaderboard(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    results = race.results.all().order_by('position')

    return render(request, 'races/race_leaderboard.html', {
        'race': race,
        'results': results
    })


def team_list(request):
    teams = Team.objects.all().order_by('name')  # Добавьте .order_by('name')
    paginator = Paginator(teams, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'races/team_list.html', {'page_obj': page_obj})
