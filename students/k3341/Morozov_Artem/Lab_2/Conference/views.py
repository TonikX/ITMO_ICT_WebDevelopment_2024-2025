from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from Conference.models import Conference, PresentationRegistration, Review
from Lab_2.forms import UserRegistrationForm, PresentationRegistrationForm, ReviewForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def conference_list(request):
    conferences = Conference.objects.all()
    return render(request, 'conference_list.html', {'conferences': conferences})

def register_for_presentation(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.conference = conference
            registration.save()
            return redirect('conference_list')
    else:
        form = PresentationRegistrationForm()
    return render(request, 'register_presentation.html', {'form': form, 'conference': conference})

def add_review(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.conference = conference
            review.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'conference': conference})

def home(request):
    return render(request, 'home.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'login.html')

def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    reviews = Review.objects.filter(conference=conference)
    presentations = PresentationRegistration.objects.filter(conference=conference)
    return render(request, 'conference_detail.html', {
        'conference': conference,
        'reviews': reviews,
        'presentations': presentations,
    })

@login_required
def register_presentation(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.user = request.user
            presentation.conference = conference
            presentation.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = PresentationRegistrationForm()
    return render(request, 'register_presentation.html', {'form': form, 'conference': conference})

@login_required
def profile(request):
    user = request.user
    presentations = PresentationRegistration.objects.filter(user=user)
    return render(request, 'profile.html', {
        'user': user,
        'presentations': presentations,
    })

@login_required
def edit_presentation(request, presentation_id):
    presentation = get_object_or_404(PresentationRegistration, id=presentation_id, user=request.user)
    if request.method == 'POST':
        form = PresentationRegistrationForm(request.POST, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PresentationRegistrationForm(instance=presentation)
    return render(request, 'edit_presentation.html', {'form': form, 'presentation': presentation})

@login_required
def delete_presentation(request, presentation_id):
    presentation = get_object_or_404(PresentationRegistration, id=presentation_id, user=request.user)
    if request.method == 'POST':
        presentation.delete()
        return redirect('home')