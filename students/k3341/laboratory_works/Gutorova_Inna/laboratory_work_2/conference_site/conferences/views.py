from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, ReviewForm, RegistrationEditForm, RegistrationForm
from .models import Conference, Registration, Review


def home(request):
    return render(request, 'base.html')
def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, 'conference_list.html', {'conferences': conferences})

def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    reviews = Review.objects.filter(conference=conference)
    return render(request, 'conference_detail.html', {'conference': conference, 'reviews': reviews})

@login_required
def register_for_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.conference = conference
            registration.save()
            return redirect('my_registrations')
    else:
        form = RegistrationForm(initial={'conference': conference})
    return render(request, 'register_for_conference.html', {'form': form, 'conference': conference})

@login_required
def add_review(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.conference = conference
            review.user = request.user
            review.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'conference': conference})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('conference_list')  # Redirect to a suitable page, e.g., the conference list
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'my_registrations.html', {'registrations': registrations})

@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        form = RegistrationEditForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('my_registrations')  # Redirect to the user's registrations list
    else:
        form = RegistrationEditForm(instance=registration)
    return render(request, 'edit_registration.html', {'form': form, 'registration': registration})

@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('conference_list')  # Redirect to a suitable page after deletion
    return render(request, 'confirm_delete_registration.html', {'registration': registration})