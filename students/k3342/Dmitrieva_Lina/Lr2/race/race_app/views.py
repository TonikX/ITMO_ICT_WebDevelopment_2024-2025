from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Racer, Team, Race
from .forms import RacerForm, CustomUserCreationForm


def racer_list(request):
    racers = Racer.objects.all()
    return render(request, 'racers_list.html', {'racers': racers})


def racer_details(request, full_name):
    try:
        racer = Racer.objects.get(full_name=full_name)
    except Racer.DoesNotExist:
        raise Http404("Гонщик не существует")

    return render(request, 'racer.html', {'racer': racer})


def race_list(request):
    races = Race.objects.all()
    return render(request, 'race_list.html', {'races': races})


def race_detail(request, name):
    race = get_object_or_404(Race, name=name)
    results = race.results.all()
    return render(request, 'race_detail.html', {'race': race, 'results': results})


def team_list(request, name):
    team = get_object_or_404(Team, name=name)
    return render(request, 'team_list.html', {'team': team})


def create_racer(request):
    form = RacerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('racers_list')
    return render(request, 'racer_form.html', {'form': form})


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')  # Перенаправление на страницу входа
    return render(request, 'register.html', {'form': form})
