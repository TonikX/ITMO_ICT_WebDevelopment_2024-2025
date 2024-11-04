from django.shortcuts import get_object_or_404
from .models import Race, Racer, RaceParticipant, Comment, Car, Fan
from .forms import UserRoleRegistrationForm, RacerRegistrationForm, FanRegistrationForm, CommentForm, \
    RaceRegistrationForm, RaceParticipantForm, RacerForm, RacerProfileForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



@login_required
def race_list(request):
    races = Race.objects.all()
    is_racer = hasattr(request.user, 'racer')
    context = {
        'races': races,
        'is_racer': is_racer,
    }

    return render(request, 'auto/race_list.html', context)


def racer_list(request):
    racers = Racer.objects.all()
    return render(request, 'auto/racer_list.html', {'racers': racers})


def racer_detail(request, racer_id):
    racer = get_object_or_404(Racer, id=racer_id)
    return render(request, 'auto/racer_detail.html', {'racer': racer})


def register(request):
    racer_form = RacerRegistrationForm()
    fan_form = FanRegistrationForm()
    if request.method == "POST":
        form = UserRoleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            if role == 'racer':
                racer_form = RacerRegistrationForm(request.POST)
                if racer_form.is_valid():
                    racer = racer_form.save(commit=False)
                    racer.user = user
                    racer.save()
                    login(request, user)
                    return redirect('race_list')
                else:
                    return render(request, 'registration/register.html', {
                        'form': form,
                        'racer_form': racer_form,
                        'fan_form': fan_form,
                    })

            elif role == 'fan':
                fan_form = FanRegistrationForm(request.POST)
                if fan_form.is_valid():
                    fan = fan_form.save(commit=False)
                    fan.user = user
                    fan.save()
                    login(request, user)
                    return redirect('race_list')
                else:
                    return render(request, 'registration/register.html', {
                        'form': form,
                        'racer_form': racer_form,
                        'fan_form': fan_form,
                    })

    else:
        form = UserRoleRegistrationForm()

    return render(request, 'registration/register.html', {
        'form': form,
        'racer_form': racer_form,
        'fan_form': fan_form,
    })


@login_required
def delete_registration(request, participant_id):
    registration = get_object_or_404(RaceParticipant, id=participant_id)
    if request.method == 'POST':
        registration.delete()
        return redirect('race_list')

    return render(request, 'auto/delete_registration.html', {'registration': registration})


@login_required
def edit_profile(request):
    racer = request.user.racer
    if request.method == 'POST':
        form = RacerProfileForm(request.POST, instance=racer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = RacerProfileForm(instance=racer)

    return render(request, 'auto/edit_profile.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    racer = None
    race_registrations = None
    try:
        racer = user.racer
        race_registrations = RaceParticipant.objects.filter(racer=racer).select_related('race')
    except Racer.DoesNotExist:
        pass

    context = {
        'user': user,
        'racer': racer,
        'race_registrations': race_registrations,
    }

    return render(request, 'auto/profile.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('race_list')
        else:
            return render(request, 'auto/login.html', {'error': 'Неправильное имя пользователя или пароль.'})
    return render(request, 'auto/login.html')


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'auto/car_detail.html', {'car': car})


@login_required
def race_registration(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    racer = request.user.racer
    if request.method == "POST":
        RaceParticipant.objects.create(racer=racer, race=race)
        return redirect('race_list')
    return render(request, 'auto/race_registration.html', {'race': race})


@login_required
def race_participants(request, race_id):
    race = Race.objects.get(id=race_id)
    participants = RaceParticipant.objects.filter(race=race).select_related('racer__car')
    context = {
        'race': race,
        'participants': participants,
    }

    return render(request, 'auto/race_participants.html', context)


def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    return render(request, 'auto/race_detail.html', {'race': race})


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)

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

    return render(request, 'auto/add_comment.html', {'form': form, 'race': race})


def race_comments(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments = race.comments.all()
    return render(request, 'auto/race_comments.html', {'race': race, 'comments': comments})


def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    participants = RaceParticipant.objects.filter(race=race)

    return render(request, 'auto/race_results.html', {'race': race, 'participants': participants})