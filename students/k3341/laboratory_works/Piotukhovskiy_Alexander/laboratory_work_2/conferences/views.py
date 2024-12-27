from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from conferences.models import Conference, ConferenceRating
from .forms import ConferenceForm, ConferenceRatingForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('conference_list')
    else:
        form = UserCreationForm()
    return render(request, 'authorization/register.html', {'form': form})

class LogoutRedirectView(View):
    def get(self, request):
        logout(request)
        return redirect('conference_list')


def conference_list(request):
    query = request.GET.get('q', '')

    conferences = Conference.objects.all()
    if query:
        conferences = conferences.filter(
            Q(title__icontains=query) |
            Q(topics__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(participation_conditions__icontains=query)
        )

    conferences = conferences.order_by('-created_at')

    paginator = Paginator(conferences, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page', 1)

    try:
        conferences_page = paginator.page(page_number)
    except PageNotAnInteger:
        conferences_page = paginator.page(1)
    except EmptyPage:
        conferences_page = paginator.page(paginator.num_pages)

    return render(request, 'conferences/conference_list.html', {
        'conferences': conferences_page,
        'paginator': paginator,
        'page_obj': conferences_page,
        'query': query
    })


def conference_detail(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ConferenceRating.objects.filter(user=request.user, conference=conference).first()

    return render(request, 'conferences/conference_detail.html', {
        'conference': conference,
        'user_rating': user_rating,
    })


@login_required
def view_participants(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    participants = conference.participants.all()

    return render(request, 'conferences/view_participants.html',
                  {'conference': conference, 'participants': participants})


@login_required
def create_conference(request):
    if request.method == "POST":
        form = ConferenceForm(request.POST)
        if form.is_valid():
            conference = form.save(commit=False)
            conference.owner = request.user
            conference.save()
            return redirect('conference_list')
    else:
        form = ConferenceForm()
    return render(request, 'conferences/create_conference.html', {'form': form})


@login_required
def edit_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)

    if conference.owner != request.user:
        return redirect('conference_detail', conference_id=conference.id)

    if request.method == "POST":
        form = ConferenceForm(request.POST, instance=conference)
        if form.is_valid():
            form.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ConferenceForm(instance=conference)

    return render(request, 'conferences/edit_conference.html', {'form': form, 'conference': conference})


@login_required
def register_for_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)
    if request.user != conference.owner:
        conference.participants.add(request.user)
    return redirect('conference_detail', conference_id=conference.id)


@login_required
def cancel_registration(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)

    if request.user in conference.participants.all():
        conference.participants.remove(request.user)

        ConferenceRating.objects.filter(user=request.user, conference=conference).delete()

    return redirect('conference_list')


@login_required
def delete_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    conference.delete()
    return redirect('conference_list')


@login_required
def rate_conference(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id)

    if request.user not in conference.participants.all():
        return redirect('conference_detail', conference_id=conference.id)

    rating = ConferenceRating.objects.filter(user=request.user, conference=conference).first()
    created = rating is None

    if request.method == "POST":
        form = ConferenceRatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.conference = conference
            rating.save()
            return redirect('conference_detail', conference_id=conference.id)
    else:
        form = ConferenceRatingForm(instance=rating)

    return render(request, 'conferences/rate_conference.html',
                  {'form': form, 'conference': conference, 'created': created})


@login_required
def view_ratings(request, conference_id):
    conference = get_object_or_404(Conference, id=conference_id, owner=request.user)
    ratings = ConferenceRating.objects.filter(conference=conference)

    return render(request, 'conferences/view_ratings.html', {'conference': conference, 'ratings': ratings})


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def all_conference_participants(request):
    conferences = Conference.objects.prefetch_related('participants').all()
    return render(request, 'conferences/all_participants.html', {'conferences': conferences})
