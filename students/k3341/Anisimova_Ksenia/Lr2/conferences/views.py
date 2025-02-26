from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Conference, Presentation, Registration, Review
from .forms import PresentationForm, RegistrationForm
from .forms import ReviewForm

@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            return redirect('my_registrations') 
    else:
        form = RegistrationForm(instance=registration)
    
    return render(request, 'edit_registration.html', {'form': form})

@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        return redirect('my_registrations') 
    return render(request, 'delete_registration.html', {'registration': registration})


@login_required
def my_registrations_view(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'my_registrations.html', {'registrations': registrations})

@login_required
def add_review(request, conference_id):
    conference = get_object_or_404(Conference, pk=conference_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.conference = conference
            review.save()
            return redirect('review_list', conference_id=conference_id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'conference': conference})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'index.html')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def index(request):
    return render(request, 'index.html')


def list_conferences(request):
    conferences = Conference.objects.all()
    registrations = Registration.objects.select_related('conference', 'user').all()
    return render(request, 'list.html', {
        'conferences': conferences,
        'registrations': registrations
    })

@login_required
def register_presentation(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.author = request.user.author
            presentation.conference = conference
            presentation.save()
            return redirect('list_conferences')
    else:
        form = PresentationForm()
    return render(request, 'register_presentation.html', {'form': form, 'conference': conference})

@login_required
def edit_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, author__user=request.user)
    if request.method == 'POST':
        form = PresentationForm(request.POST, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('list_conferences')
    else:
        form = PresentationForm(instance=presentation)
    return render(request, 'edit_presentation.html', {'form': form, 'presentation': presentation})

@login_required
def delete_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id, author__user=request.user)
    if request.method == 'POST':
        presentation.delete()
        return redirect('list_conferences')
    return render(request, 'delete_presentation.html', {'presentation': presentation})


def review_list(request, conference_id):
    reviews = Review.objects.filter(conference_id=conference_id).order_by('-comment_date')
    conference = Conference.objects.get(pk=conference_id)
    return render(request, 'reviews_list.html', {'reviews': reviews, 'conference': conference})


@login_required
def create_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.save()
            return redirect('my_registrations')
    else:
        form = RegistrationForm()
    return render(request, 'create_registration.html', {'form': form})