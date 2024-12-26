from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Race, Registration, Comment


def race_list(request):
    query = request.GET.get('q', '')
    races = Race.objects.all()

    if query:
        races = races.filter(Q(name__icontains=query) | Q(result__icontains=query))

    paginator = Paginator(races, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_registrations = Registration.objects.filter(user=request.user) if request.user.is_authenticated else []
    registration_dict = {reg.race_id: reg for reg in user_registrations}

    return render(request, 'races/race_list.html', {
        'page_obj': page_obj,
        'registration_dict': registration_dict,
        'query': query
    })


@login_required
def register_racer(request):
    if request.method == 'POST':
        race_id = request.POST.get('race_id')
        race = get_object_or_404(Race, pk=race_id)
        if Registration.objects.filter(race=race, user=request.user).exists():
            messages.error(request, 'Вы уже зарегистрированы на эту гонку.')
            return redirect('race_list')
        try:
            Registration.objects.create(race=race, user=request.user)
            messages.success(request, f'Вы успешно зарегистрировались на гонку "{race.name}".')
        except IntegrityError:
            messages.error(request, 'Произошла ошибка при регистрации. Попробуйте позже.')
        return redirect('race_list')
    return redirect('race_list')


@login_required
def delete_registration(request, pk):
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('race_list')
    return render(request, 'races/delete_registration.html', {'registration': registration})


@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.save()
            return redirect('race_detail', pk=comm.race.pk)
    else:
        form = CommentForm()
    return render(request, 'races/add_comment.html', {'form': form})


def race_detail(request, pk):
    race = get_object_or_404(Race, pk=pk)
    registrations = Registration.objects.filter(race=race)
    comments = Comment.objects.filter(race=race)
    return render(request, 'races/race_detail.html', {
        'race': race,
        'registrations': registrations,
        'comments': comments,
    })
