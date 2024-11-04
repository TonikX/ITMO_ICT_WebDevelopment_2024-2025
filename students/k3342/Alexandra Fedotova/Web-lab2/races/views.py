from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import RegisterForm, ParticipantProfileForm, CommentForm
from .models import Race, Registration, Participant, Team, Comment, RaceResult

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)

            # Создаем профиль участника
            if user.role == 'participant':
                experience = form.cleaned_data.get('experience')
                Participant.objects.create(user=user, experience=experience)

            # Перенаправляем в личный кабинет
            return redirect('participant_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def participant_dashboard(request):
    participant = get_object_or_404(Participant, user=request.user)
    registrations = Registration.objects.filter(participant=participant)
    races = Race.objects.all().order_by('date', 'start_time')  # Все гонки

    context = {
        'registrations': registrations,
        'races': races,
        'participant': participant,
    }
    return render(request, 'participant_dashboard.html', context)

@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participant = get_object_or_404(Participant, user=request.user)

    registration, created = Registration.objects.get_or_create(participant=participant, race=race)

    if created:
        print("Регистрация успешно создана")
    else:
        print("Регистрация уже существовала")

    return redirect('participant_dashboard')

@login_required
def unregister_from_race(request, registration_id):
    try:
        registration = Registration.objects.get(id=registration_id, participant__user=request.user)
        registration.delete()
        print("Регистрация успешно удалена")
    except Registration.DoesNotExist:
        raise Http404("Регистрация не найдена или у вас нет прав на её удаление")

    return redirect('participant_dashboard')


@login_required
def profile_data(request):
    participant = get_object_or_404(Participant, user=request.user)
    teams = Team.objects.all()  

    if request.method == "POST":
        form = ParticipantProfileForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            print("Форма сохранена!") 
            return redirect('participant_dashboard')
        else:
            print("Ошибки формы:", form.errors)  
    else:
        form = ParticipantProfileForm(instance=participant)

    return render(request, 'edit_profile.html', {
        'form': form,
        'participant': participant,
        'teams': teams  
    })


@login_required
def registrations_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registrations = Registration.objects.filter(race=race).select_related('participant')

    context = {
        'race': race,
        'registrations': registrations,
    }
    return render(request, 'registrations_for_race.html', context)


def all_races(request):
    races = Race.objects.all().order_by('date', 'start_time')
    print(races) 
    return render(request, 'all_races.html', {'races': races})

def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    race_results = RaceResult.objects.filter(race=race).select_related('team')  

    context = {
        'race': race,
        'race_results': race_results,
    }
    return render(request, 'race_results.html', context)

@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.user = request.user
            comment.save()
            return redirect('race_comments', race_id=race.id)
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'race': race})


@login_required
def race_comments(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments = Comment.objects.filter(race=race)
    return render(request, 'race_comments.html', {'race': race, 'comments': comments})