from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Race, Racer, Registration, Comment, RaceResult
from .forms import RegistrationForm, CommentForm, UserRegistrationForm, RacerProfileForm, AutomobileForm, UnregisterForm, UserUpdateForm, RacerProfileUpdateForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('race_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class LogoutUser(View):

    def get(self, request):
        logout(request)
        return redirect('race_list')


class RaceListView(ListView):
    model = Race
    template_name = 'race_list.html'
    context_object_name = 'races'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['upcoming_races'] = Race.objects.filter(date__gte=now).order_by('-date')
        context['past_races'] = Race.objects.filter(date__lt=now).exclude(result="").order_by('-date')
        context['has_racer_profile'] = hasattr(self.request.user, 'racer') if self.request.user.is_authenticated else False

        return context


class RaceDetailView(DetailView):
    model = Race
    template_name = 'race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['is_upcoming'] = self.object.date >= now

        if context['is_upcoming']:
            context['registered_racers'] = self.object.registrations.all()
        else:
            context['race_results'] = RaceResult.objects.filter(race=self.object).order_by('place')

        context['unregister_form'] = UnregisterForm()

        # Проверка, зарегистрирован ли пользователь на гонку
        if self.request.user.is_authenticated:
            # Проверка на наличие профиля гонщика
            context['has_racer_profile'] = hasattr(self.request.user, 'racer')
            if context['has_racer_profile']:
            # Выполняем проверку регистрации только если профиль гонщика существует
                context["is_registered"] = Registration.objects.filter(
                    race=self.object, racer=self.request.user.racer
                ).exists()
            else:
                context["is_registered"] = False
        else:
            context["is_registered"] = False

        return context


class RaceRegistrationView(LoginRequiredMixin, CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'register_race.html'

    def form_valid(self, form):
        # Проверка на наличие профиля гонщика
        if not hasattr(self.request.user, 'racer'):
            return HttpResponseRedirect(reverse('create_racer_profile'))

        race = get_object_or_404(Race, id=self.kwargs['race_id'])
        form.instance.race = race
        form.instance.racer = self.request.user.racer
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['racer'] = self.request.user.racer  # Передаем профиль гонщика в форму
        return kwargs

    def get_success_url(self):
        return reverse('race_detail', args=[self.kwargs['race_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = get_object_or_404(Race, id=self.kwargs['race_id'])
        return context


class RaceUnregisterView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        race = get_object_or_404(Race, id=self.kwargs['race_id'])

        if not hasattr(request.user, 'racer'):
            messages.warning(request, "У вас нет профиля гонщика. Сначала создайте его.")
            return redirect('create_racer_profile')

        registration = Registration.objects.filter(race=race, racer=request.user.racer).first()

        if registration:
            registration.delete()
            messages.success(request, "Вы успешно отменили регистрацию на гонку.")
        else:
            messages.warning(request, "Вы не зарегистрированы на эту гонку.")

        return redirect('race_detail', pk=race.id)


class RacerProfileCreateView(LoginRequiredMixin, CreateView):
    model = Racer
    template_name = 'create_racer_profile.html'
    form_class = RacerProfileForm
    success_url = reverse_lazy('race_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RacerProfileView(LoginRequiredMixin, DetailView):
    model = Racer
    template_name = 'racer_profile.html'
    context_object_name = 'racer'

    def get_object(self):
        return get_object_or_404(Racer, user=self.request.user)

    def post(self, request, *args, **kwargs):
        automobile_form = AutomobileForm(request.POST)
        if automobile_form.is_valid():
            car = automobile_form.save()
            self.get_object().cars.add(car)
            messages.success(request, "Автомобиль успешно добавлен к профилю.")
            return redirect('racer_profile', pk=self.get_object().id)
        else:
            messages.error(request, "Ошибка при добавлении автомобиля. Проверьте форму.")
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['automobile_form'] = AutomobileForm()
        return context


class RacerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Racer
    template_name = 'edit_racer_profile.html'
    context_object_name = 'racer'
    form_class = RacerProfileUpdateForm

    def get_object(self, queryset=None):
        return get_object_or_404(Racer, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
            form.save()
            return redirect('racer_profile', pk=self.request.user.racer.pk)
        else:
            self.form_invalid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.race = get_object_or_404(Race, id=self.kwargs['race_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('race_detail', args=[self.kwargs['race_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = get_object_or_404(Race, id=self.kwargs['race_id'])
        return context


class EditRaceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Race
    fields = ['name', 'date', 'result']
    template_name = 'edit_race.html'
    success_url = reverse_lazy('race_list')

    def test_func(self):
        return self.request.user.is_staff


class DeleteRaceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Race
    template_name = 'delete_race.html'
    context_object_name = 'race'
    success_url = reverse_lazy('race_list')

    def test_func(self):
        return self.request.user.is_staff


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        race_id = comment.race.id
        if not request.user.is_staff:
            return redirect('race_detail', pk=race_id)

        comment.delete()
        return redirect('race_detail', pk=race_id)

    def test_func(self):
        return self.request.user.is_staff
