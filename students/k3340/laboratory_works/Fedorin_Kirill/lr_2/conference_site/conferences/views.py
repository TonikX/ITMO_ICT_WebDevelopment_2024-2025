import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationUpdateForm, ReviewForm, UserRegisterForm
from .models import Conference, Registration


@login_required
def unregister_from_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    registration = Registration.objects.filter(conference=conference, user=request.user).first()
    if registration:
        registration.delete()
        messages.success(request, f'You have successfully unregistered from {conference.title}.')
    else:
        messages.error(request, 'You are not registered for this conference.')
    return redirect('conference_detail', conference_id=conference_id)

def conference_list(request):
    query = request.GET.get('q')
    conferences = Conference.objects.filter(title__icontains=query, start_date__gte=datetime.datetime.now(tz=datetime.timezone.utc).date()) if query\
        else Conference.objects.all() # Поиск по названию конференции
    conferences = conferences.order_by('start_date')
    paginator = Paginator(conferences, 10)  # Показывать по 10 конференций на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'conferences/conference_list.html', {'page_obj': page_obj, 'query': query})

def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    reviews = conference.review_set.all()
    participants = Registration.objects.filter(conference=conference)
    registration_exists = participants.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'conferences/conference_detail.html', {
        'conference': conference,
        'reviews': reviews,
        'participants': participants,
        'registration_exists': registration_exists,
    })


@login_required
def add_review(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    registration = Registration.objects.filter(conference=conference, user=request.user).exists()
    if not registration:
        messages.error(request, 'You must be registered and have attended the conference to leave a review.')
        return redirect('conference_detail', conference_id=conference_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.conference = conference
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added!')
            return redirect('conference_detail', conference_id=conference_id)
    else:
        form = ReviewForm()
    return render(request, 'conferences/add_review.html', {'form': form, 'conference': conference})

@login_required
def edit_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        form = RegistrationUpdateForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your registration has been updated!')
            return redirect('conference_list')
    else:
        form = RegistrationUpdateForm(instance=registration)
    return render(request, 'conferences/edit_registration.html', {'form': form})

@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.delete()
        messages.success(request, 'Your registration has been deleted!')
        return redirect('conference_list')
    return render(request, 'conferences/delete_registration.html', {'registration': registration})

@login_required
def register_for_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    registration, created = Registration.objects.get_or_create(user=request.user, conference=conference)
    if created:
        messages.success(request, f'You have successfully registered for {conference.title}.')
    else:
        messages.info(request, f'You are already registered for {conference.title}.')
    return redirect('conference_detail', conference_id=conference_id)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Переадресация на страницу входа
    else:
        form = UserRegisterForm()
    return render(request, 'conferences/register.html', {'form': form})
