from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from race_panel.models import Race, Racer, Registration, Car, Comment, RaceTime


class RaceListView(ListView):
    model = Race
    template_name = 'race/root.html'
    context_object_name = 'races'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.session.get('user_id', None)
        try:
            user = Racer.objects.get(pk=user)  # checked in dispatch
            registrations = Registration.objects.filter(racer=user)
        except Registration.DoesNotExist:
            registrations = Race.objects.none()

        queryset = (Race.objects.filter(
            dt_due_register__gte=datetime.now()
        )
        .exclude(id__in=registrations.values_list('event_id', flat=True))
        .order_by(
            'dt_due_register',
        )).all()
        return queryset

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', None)
        if not (Racer.objects.filter(pk=user_id).exists()
                and self.get_queryset().exists()):
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class YourRaceListView(ListView):
    model = Race
    template_name = 'race/root.html'
    context_object_name = 'races'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.session.get('user_id', None)
        try:
            user = Racer.objects.get(pk=user)  # checked in dispatch
            registrations = Registration.objects.filter(racer=user)
        except Registration.DoesNotExist:
            registrations = Race.objects.none()

        queryset = (Race.objects.filter(
            id__in=registrations.values_list('event_id', flat=True)
        )
        .order_by(
            'dt_due_register',
        )).all()
        return queryset

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', None)
        if not (Racer.objects.filter(pk=user_id).exists()
                and self.get_queryset().exists()):
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class HistoryRaceListView(ListView):
    model = Race
    template_name = 'race/root.html'
    context_object_name = 'races'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.session.get('user_id', None)
        try:
            user = Racer.objects.get(pk=user)  # checked in dispatch
            registrations = Registration.objects.filter(racer=user)
        except Registration.DoesNotExist:
            registrations = Race.objects.none()

        queryset = (Race.objects.filter(
            dt_due_register__lte=datetime.now()
        )
        .order_by(
            'dt_due_register',
        )).all()
        return queryset

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', None)
        if not (Racer.objects.filter(pk=user_id).exists()
                or self.get_queryset().exists()):
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class RaceDetailView(DetailView):
    model = Race
    template_name = 'race/detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = context['race']
        user_id = self.request.session.get('user_id', None)
        user_model = Racer.objects.get(pk=user_id)
        context.update({'user': user_model})
        if (registration := Registration.objects.filter(racer=user_model, event=race)).exists():
            context.update({'registration': registration.first()})
        context['comments'] = Comment.objects.filter(race=race)
        context['results'] = RaceTime.objects.filter(event=race)
        return context


class RegistrationCreateView(CreateView):
    model = Registration
    template_name = 'race/register.html'
    fields = ['car']
    success_url = reverse_lazy('race')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        racer_id = self.request.session.get('user_id', None)

        try:
            racer = Racer.objects.get(pk=racer_id)
            form.fields['car'].queryset = Car.objects.filter(car_owner=racer)
        except Racer.DoesNotExist:
            return redirect(reverse_lazy('login'))

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['race'] = Race.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        racer_id = self.request.session.get('user_id')
        try:
            racer = Racer.objects.get(pk=racer_id)
            form.instance.racer = racer
        except Racer.DoesNotExist:
            return redirect(reverse_lazy('login'))
        form.instance.event = self.get_context_data()['race']
        form.dt_register = datetime.now()
        return super().form_valid(form)


class RegistrationDeleteView(DeleteView):
    model = Registration
    template_name = 'race/confirm_delete.html'
    success_url = reverse_lazy('race')

    def get_object(self, queryset=None):
        event_id = self.kwargs.get('pk')

        race = self.model.objects.get(event_id=event_id, racer=self.request.session.get('user_id'))
        return race


class CommentCreate(CreateView):
    model = Comment
    template_name = 'race/create_comment.html'
    fields = ['comment_type', 'header', 'text', 'rating']
    success_url = reverse_lazy('race')

    def form_valid(self, form):
        user_id = self.request.session.get('user_id', None)
        event_id = self.kwargs.get('pk')
        form.instance.race = Race.objects.get(pk=event_id)
        form.instance.user = Racer.objects.get(pk=user_id)
        form.instance.dt_written = datetime.now()
        return super().form_valid(form)
