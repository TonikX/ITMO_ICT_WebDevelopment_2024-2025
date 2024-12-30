from django.forms import forms
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import OwnerForm, CarCreateForm
from .models import Owner, Car


def home(request):
    return render(request, 'home.html')


def owner_detail(request,owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner':owner})


def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners':owners})


class CarListView(ListView):
    model = Car
    template_name = "car_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        cars = Car.objects.all()
        if not cars.exists():
            raise Http404("No cars available")
        return cars


class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"
    context_object_name = "car"

    def get_object(self):
        car_id = self.kwargs.get('pk')
        car = Car.objects.filter(pk=car_id).first()
        if not car:
            raise Http404(f"Car with id {car_id} does not exist")
        return car


def add_owner(request):
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('owner_list'))
    context['form'] = form
    return render(request, 'add_owner.html', context)


class CarCreateView(CreateView):
    model = Car
    fields = [
        'state_num',
        'brand',
        'model',
        'color'
    ]
    template_name = 'add_car.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
    model = Car
    success_url = reverse_lazy('car_list')
    template_name = 'delete_car.html'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['state_num', 'brand', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

    def get_object(self, queryset=None):
        car_id = self.kwargs.get('pk')
        car = Car.objects.filter(pk=car_id).first()
        if not car:
            raise Http404(f"Car with id {car_id} does not exist")
        return car