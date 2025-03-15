from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm, PresentationForm, ReviewForm, RegistrationUpdateForm
from .models import Conference, Registration
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('conf_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def conferences_list(request):
    confs = Conference.objects.all()
    data = []
    if request.user.is_authenticated:
        for conf in confs:
            data.append({
                'conf': conf,
                'registration': Registration.objects.filter(conference=conf, user=request.user).first()
            })
        return render(request, 'conf_list.html', {'confs': data})
    return render(request, 'conf_list.html', {'confs': confs})


def presentations_list(request, conf_id):
    conf = get_object_or_404(Conference, id=conf_id)
    presentations = conf.presentations.all()
    return render(request, 'presentations_list.html', {'conf': conf, 'presentations': presentations})


@login_required
def make_presentation(request, conf_id):
    conf = get_object_or_404(Conference, id=conf_id)

    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.author = request.user
            presentation.conference = conf
            presentation.save()

            registration, created = Registration.objects.get_or_create(
                user_id=request.user.id,
                conference_id=conf.id,
                defaults={'is_author': True, 'presentation': presentation}
            )

            if not created:
                registration.is_author = True
                registration.presentation = presentation
                registration.save()

            return redirect('my_registrations')
    else:
        form = PresentationForm()

    return render(request, 'make_presentation.html', {'form': form, 'conf': conf})


@login_required
def enroll(request, conf_id):
    conf = get_object_or_404(Conference, id=conf_id)

    Registration.objects.get_or_create(
        user=request.user,
        conference=conf,
    )

    return redirect('conf_list')


@login_required
def my_registrations(request):
    registrations = request.user.registrations.all()
    return render(request, 'my_registrations.html', {'registrations': registrations})


@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        form = RegistrationUpdateForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('my_registrations')
    else:
        form = RegistrationUpdateForm(instance=registration)
    return render(request, 'edit_registration.html', {'form': form})


@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('my_registrations')
    return render(request, 'delete_registration.html', {'registration': registration})


@login_required
def add_review(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.registration = registration
            review.save()
            return redirect('my_registrations')
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})


def participants(request):
    last_month = timezone.now() - timedelta(days=30)
    registrations = Registration.objects.filter(conference__starting_at__gte=last_month)
    return render(request, 'participants.html', {'registrations': registrations})
