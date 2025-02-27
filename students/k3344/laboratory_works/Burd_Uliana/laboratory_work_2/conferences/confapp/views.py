from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.utils import timezone

from .forms import UserRegistrationForm, RegistrationForm, ReviewForm
from .models import Conference, Registration, UserProfile, Review
from django.contrib.auth.decorators import login_required


def create_user_profile(user):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return UserProfile.objects.create(user=user)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('confapp:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration_form.html', {'form': form})


@login_required
def conference_detail(request, conference_id):
    conference = Conference.objects.get(pk=conference_id)
    return render(request, 'conference_detail.html', {'conference': conference})


@login_required
def home(request):
    conferences = Conference.objects.all()
    return render(request, 'home.html', {'conferences': conferences})


@login_required
def conference_participants(request, conference_id):
    conference = Conference.objects.get(pk=conference_id)
    participants = Registration.objects.filter(conference=conference)
    return render(request, 'conference_participants.html', {'conference': conference, 'participants': participants})


@login_required
def register_for_conference(request, conference_id):
    conference = Conference.objects.get(pk=conference_id)
    user = request.user

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.conference = conference
            registration.user = user
            registration.save()
            return redirect('confapp:home')
    else:
        form = RegistrationForm()

    return render(request, 'register_for_conference.html', {'conference': conference, 'form': form})


@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('confapp:user_registrations')

    else:
        form = RegistrationForm(instance=registration)

    return render(request, 'edit_registration.html', {'form': form})


@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)

    if request.method == "POST":
        registration.delete()
        return redirect('confapp:user_registrations')

    return render(request, 'delete_registration.html', {'registration': registration})


@login_required
def write_review(request, conference_id):
    conference = Conference.objects.get(pk=conference_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.conference = conference
            review.user = request.user
            review.date = timezone.now()
            review.save()
            return redirect('confapp:home')

    else:
        form = ReviewForm()

    reviews = Review.objects.filter(conference=conference)

    return render(request, 'write_review.html', {'form': form, 'conference': conference, 'reviews': reviews})


@login_required
def user_registrations(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'user_registrations.html', {'registrations': registrations})