from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from django.utils import timezone
from .models import Race, Racer, RaceRegistration, Comment, RaceResult, Team, Car
from .forms import RacingUserCreationForm, RacerProfileForm, RaceRegistrationForm, CommentForm, RaceSearchForm


def is_admin(user):
    return user.is_staff


def home(request):
    recent_races = Race.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')[:5]
    top_racers = Racer.objects.order_by('-wins_count')[:5]
    teams = Team.objects.all()[:5]

    context = {
        'recent_races': recent_races,
        'top_racers': top_racers,
        'teams': teams,
    }
    return render(request, 'home.html', context)


class RegisterView(CreateView):
    form_class = RacingUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация успешна! Теперь вы можете войти в систему.')
        return response


class RaceListView(ListView):
    model = Race
    template_name = 'races/race_list.html'
    context_object_name = 'races'
    paginate_by = 6

    def get_queryset(self):
        queryset = Race.objects.filter(is_active=True).order_by('-start_date')

        form = RaceSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            location = form.cleaned_data.get('location')
            race_type = form.cleaned_data.get('race_type')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if location:
                queryset = queryset.filter(location__icontains=location)
            if race_type:
                queryset = queryset.filter(race_type=race_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = RaceSearchForm(self.request.GET)
        return context


class RaceDetailView(DetailView):
    model = Race
    template_name = 'races/race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.get_object()

        context['registrations'] = RaceRegistration.objects.filter(race=race).select_related('racer', 'car')
        context['results'] = RaceResult.objects.filter(
            race_registration__race=race
        ).select_related('race_registration__racer').order_by('position')

        context['comments'] = Comment.objects.filter(race=race).select_related('author').order_by('-comment_date')
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated and hasattr(self.request.user, 'racer'):
            context['is_registered'] = RaceRegistration.objects.filter(
                race=race,
                racer=self.request.user.racer
            ).exists()

        return context


@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if not hasattr(request.user, 'racer'):
        messages.error(request, 'Сначала создайте профиль гонщика!')
        return redirect('create_racer_profile')

    racer = request.user.racer

    if RaceRegistration.objects.filter(race=race, racer=racer).exists():
        messages.warning(request, 'Вы уже зарегистрированы на эту гонку!')
        return redirect('race_detail', pk=race_id)

    if request.method == 'POST':
        form = RaceRegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.race = race
            registration.racer = racer
            registration.save()
            messages.success(request, 'Регистрация на гонку успешна! Ожидайте подтверждения.')
            return redirect('race_detail', pk=race_id)
    else:
        form = RaceRegistrationForm(user=request.user)

    context = {
        'form': form,
        'race': race,
    }
    return render(request, 'races/race_register.html', context)


@login_required
def create_racer_profile(request):
    if hasattr(request.user, 'racer'):
        messages.info(request, 'Профиль гонщика уже создан!')
        return redirect('profile')

    if request.method == 'POST':
        form = RacerProfileForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            racer.user = request.user
            racer.save()
            messages.success(request, 'Профиль гонщика успешно создан!')
            return redirect('profile')
    else:
        form = RacerProfileForm()

    return render(request, 'profile/create_racer.html', {'form': form})


@login_required
def profile(request):
    racer = getattr(request.user, 'racer', None)
    registrations = RaceRegistration.objects.filter(racer=racer).select_related('race', 'car') if racer else None

    context = {
        'racer': racer,
        'registrations': registrations,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен!')

    return redirect('race_detail', pk=race_id)


@login_required
@user_passes_test(is_admin)
def race_results_admin(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registrations = RaceRegistration.objects.filter(race=race).select_related('racer', 'car')

    if request.method == 'POST':
        for registration in registrations:
            finish_time = request.POST.get(f'finish_time_{registration.id}')
            position = request.POST.get(f'position_{registration.id}')
            best_lap_time = request.POST.get(f'best_lap_time_{registration.id}')
            points = request.POST.get(f'points_{registration.id}')
            dnf = request.POST.get(f'dnf_{registration.id}')

            result, created = RaceResult.objects.get_or_create(race_registration=registration)

            if finish_time:
                result.finish_time = finish_time
            if position:
                result.position = int(position)
            if best_lap_time:
                result.best_lap_time = best_lap_time
            if points:
                result.points = int(points)
            result.dnf = bool(dnf)
            result.save()

        messages.success(request, 'Результаты гонки сохранены!')
        return redirect('race_results_admin', race_id=race_id)

    context = {
        'race': race,
        'registrations': registrations,
    }
    return render(request, 'admin/race_results.html', context)


class RacerListView(ListView):
    model = Racer
    template_name = 'racers/racer_list.html'
    context_object_name = 'racers'
    paginate_by = 12

    def get_queryset(self):
        queryset = Racer.objects.select_related('user', 'team')

        # Сортировка
        sort = self.request.GET.get('sort', 'name')
        if sort == 'wins':
            queryset = queryset.order_by('-wins_count')
        elif sort == 'experience':
            queryset = queryset.order_by('-user__experience_years')
        else:  # name
            queryset = queryset.order_by('user__first_name', 'user__last_name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика для отображения
        context['total_wins'] = Racer.objects.aggregate(total_wins=models.Sum('wins_count'))['total_wins'] or 0
        context['pro_racers_count'] = Racer.objects.filter(racer_class='Pro').count()
        context['teams_count'] = Team.objects.count()

        return context


class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 8

    def get_queryset(self):
        queryset = Team.objects.all()

        # Сортировка
        sort = self.request.GET.get('sort', 'name')
        if sort == 'country':
            queryset = queryset.order_by('country', 'name')
        elif sort == 'date':
            queryset = queryset.order_by('founded_date')
        else:  # name
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика для отображения
        context['total_racers'] = Racer.objects.count()
        context['total_cars'] = Car.objects.count()

        # Подсчет побед для каждой команды
        team_wins = {}
        for team in context['teams']:
            wins = Racer.objects.filter(team=team).aggregate(total_wins=models.Sum('wins_count'))['total_wins'] or 0
            team_wins[team.id] = wins
        context['team_wins'] = team_wins

        return context


class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()

        context['racers'] = Racer.objects.filter(team=team).select_related('user')
        context['cars'] = Car.objects.filter(team=team)

        # Подсчет общей статистики
        total_wins = Racer.objects.filter(team=team).aggregate(total_wins=models.Sum('wins_count'))['total_wins'] or 0
        context['total_wins'] = total_wins

        # Подсчет участий в гонках (упрощенно)
        total_participations = RaceRegistration.objects.filter(racer__team=team).count()
        context['total_participations'] = total_participations

        # Последние гонки команды
        recent_races = Race.objects.filter(
            raceregistration__racer__team=team
        ).distinct().order_by('-start_date')[:5]
        context['recent_races'] = recent_races

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        context['racers'] = Racer.objects.filter(team=team)
        context['cars'] = Car.objects.filter(team=team)
        return context