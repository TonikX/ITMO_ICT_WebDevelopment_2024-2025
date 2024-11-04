from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from race_panel.models import Racer, Car


class RacerCarView(ListView):
    model = Car
    context_object_name = 'RacerCars'
    template_name = 'cars/root.html'

    def get_queryset(self):
        user = self.request.session.get('user_id', None)
        try:
            user = Racer.objects.get(pk=user)
            return Car.objects.filter(car_owner=user)
        except Racer.DoesNotExist:
            return None

    def dispatch(self, request, *args, **kwargs):
        if self.get_queryset() is None:
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class CarUpdateView(UpdateView):
    model = Car
    fields = ['model_name', 'license_plate', 'info']
    template_name = 'cars/edit.html'
    success_url = reverse_lazy('cars')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(car_owner=self.request.session.get('user_id', None))

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise Http404("You do not have permission to edit this car.")
        return super().dispatch(request, *args, **kwargs)


class CarDeleteView(DeleteView):
    model = Car
    model_name = 'car'
    template_name = 'cars/confirm_delete.html'
    success_url = reverse_lazy('cars')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(car_owner=self.request.session.get('user_id', None))

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise Http404("You do not have permission to edit this car.")
        return super().dispatch(request, *args, **kwargs)


class CarCreateView(CreateView):
    model = Car
    template_name = 'cars/create_car.html'
    fields = ['model_name', 'license_plate', 'info']
    success_url = reverse_lazy('cars')

    def form_valid(self, form):
        form.instance.car_owner = (
            Racer.objects.get(pk=self.request.session.get('user_id', None)))
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        try:
            Racer.objects.get(pk=self.request.session.get('user_id', None))
            return super().get(*args, **kwargs)
        except Racer.DoesNotExist:
            return redirect(reverse_lazy('login'))
