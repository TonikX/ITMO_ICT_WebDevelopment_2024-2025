from datetime import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, DeleteView

from conferences.forms import UserRegistrationForm
from conferences.models import Conference, Speaker, Registration, Review


# Create your views here.
def index(request):
    return render(request, 'index.html')


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


class AccountDetailsView(LoginRequiredMixin, DetailView):
    template_name = 'account/details.html'
    model = User

    def get_object(self):
        return self.request.user


class ConferenceListView(ListView):
    model = Conference
    template_name = 'conferences/list.html'

    def get_queryset(self):
        if self.request.GET.get('archive', False):
            return Conference.objects.filter(event_date__lte=datetime.today().date())

        return Conference.objects.filter(event_date__gt=datetime.today().date())

    def get_context_data(self, **kwargs):
        context = super(ConferenceListView, self).get_context_data(**kwargs)
        context['archive'] = bool(self.request.GET.get('archive', False))
        return context


class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conferences/details.html'

    def get_context_data(self, **kwargs):
        context = super(ConferenceDetailView, self).get_context_data(**kwargs)
        context['can_register'] = context['object'].event_date >= datetime.today().date()
        context['can_propose'] = context['object'].due_register >= datetime.today().date()
        context['speakers'] = Speaker.objects.filter(conference=context['object'], confirmed=True)

        return context


class SpeakerCreateView(LoginRequiredMixin, CreateView):
    model = Speaker
    template_name = 'conferences/speaker.html'
    fields = [
        'topic',
        'description',
    ]

    def get_context_data(self, **kwargs):
        context = super(SpeakerCreateView, self).get_context_data(**kwargs)
        context['conference'] = get_object_or_404(Conference, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs.get('pk'))

        if Speaker.objects.filter(speaker=self.request.user, conference=conference).exists():
            messages.warning(self.request, "You have already registered for this conference.")
            return HttpResponseRedirect(self.get_success_url())

        form.instance.conference = conference
        form.instance.speaker = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.kwargs.get('pk')})


class RegistrationCreateView(LoginRequiredMixin, CreateView):
    model = Registration
    template_name = 'conferences/registration.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super(RegistrationCreateView, self).get_context_data(**kwargs)
        context['conference'] = get_object_or_404(Conference, pk=self.kwargs.get('pk'))

        return context

    def form_valid(self, form):
        conference = get_object_or_404(Conference, pk=self.kwargs.get('pk'))

        if Registration.objects.filter(user=self.request.user, conference=conference).exists():
            messages.warning(self.request, "You have already registered for this conference.")
            return HttpResponseRedirect(self.get_success_url())

        form.instance.conference = conference
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('conference_detail', kwargs={'pk': self.kwargs.get('pk')})


class RegistrationListView(LoginRequiredMixin, ListView):
    model = Registration
    template_name = 'registrations/list.html'

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.today().date()
        return context


class RegistrationDeleteView(LoginRequiredMixin, DeleteView):
    model = Registration
    template_name = 'registrations/delete.html'
    success_url = '/registrations/'

    def get_queryset(self):
        return Registration.objects.filter(
            user=self.request.user,
            conference__event_date__gt=datetime.today().date()
        )


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'registrations/create.html'
    fields = ['rating', 'text']
    success_url = '/registrations/'

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        context['registration'] = get_object_or_404(
            Registration,
            pk=self.kwargs.get('pk'),
            conference__event_date__lt=datetime.today().date()
        )
        return context

    def form_valid(self, form):
        registration = get_object_or_404(Registration, pk=self.kwargs.get('pk'))
        form.instance.registration = registration
        return super().form_valid(form)


class SpeakerListView(LoginRequiredMixin, ListView):
    model = Speaker
    template_name = 'speaker/list.html'

    def get_queryset(self):
        return Speaker.objects.filter(speaker=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.today().date()
        return context
