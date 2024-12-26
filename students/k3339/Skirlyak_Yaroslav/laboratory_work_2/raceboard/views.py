from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserRegistrationForm, CommentForm
from .models import Race, RaceResult, Registration, Comment
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from .utils import participant_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def race_list(request):
    races = Race.objects.all()
    return render(request, 'raceboard/race_list.html', {'races': races})


@login_required
def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    results = RaceResult.objects.filter(race=race).order_by('position')
    comments = Comment.objects.filter(race=race).order_by('-created_at')
    participants = Registration.objects.filter(race=race).select_related('participant__user')
    form = CommentForm()

    # Проверка регистрации пользователя
    is_registered = False
    if request.user.is_authenticated and hasattr(request.user, 'participant'):
        is_registered = Registration.objects.filter(participant=request.user.participant, race=race).exists()

    return render(request, 'raceboard/race_detail.html', {
        'race': race,
        'results': results,
        'comments': comments,
        'participants': participants,
        'is_registered': is_registered,
        'form': form,  # Передаём форму в шаблон
    })

@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.race = race
            comment.save()
            return redirect('race_detail', race_id=race.id)
    else:
        form = CommentForm()
    return render(request, 'raceboard/add_comment.html', {'race': race, 'form': form})

@login_required
def register_for_race(request, race_id):
    race = Race.objects.get(pk=race_id)
    participant = request.user.participant
    Registration.objects.create(participant=participant, race=race)
    return redirect('race_detail', race_id=race_id)

@login_required
@participant_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participant = request.user.participant  # Получаем профиль участника

    # Проверяем, что пользователь ещё не зарегистрирован
    if Registration.objects.filter(participant=participant, race=race).exists():
        return render(request, 'raceboard/error.html', {
            'message': 'Вы уже зарегистрированы на эту гонку.'
        })

    # Регистрируем пользователя на гонку
    Registration.objects.create(participant=participant, race=race)
    return redirect('race_detail', race_id=race.id)

@login_required
@participant_required
def unregister_from_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participant = request.user.participant  # Получаем профиль участника

    # Удаляем регистрацию, если она существует
    registration = Registration.objects.filter(participant=participant, race=race).first()
    if registration:
        registration.delete()
    return redirect('race_detail', race_id=race.id)

@login_required
@participant_required
def my_registrations(request):
    # Показываем все регистрации текущего участника
    registrations = Registration.objects.filter(participant=request.user.participant)
    return render(request, 'raceboard/my_registrations.html', {'registrations': registrations})