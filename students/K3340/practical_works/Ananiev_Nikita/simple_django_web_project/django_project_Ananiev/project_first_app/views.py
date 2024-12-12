from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import CarOwner, Car, Ownership
from .forms import *

def owner_data(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'car_owner.html', {'owner': owner})


def owners_list(request):
    context = {}
    try:
        context["owners"] = CarOwner.objects.all()
    except CarOwner.DoesNotExist:
        raise Http404("No owners found")
    return render(request, 'owners_list.html', context)


class CarData(DetailView):
    model = Car
    template_name = 'car.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ownerships"] = Ownership.objects.filter(car=self.object)
        return context


class CarList(ListView):
    model = Car
    template_name = 'cars_list.html'
    context_object_name = 'cars'


def add_car_owner(request):
    context = {}
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CarOwnerForm()
    context['form'] = form
    return render(request, 'add_owner.html', context)


class AddCar(CreateView):
    model = Car
    template_name = 'add_car.html'
    fields = ['brand', 'model', 'license_plate', 'color']
    success_url = '/car/list/'


class UpdateCar(UpdateView):
    model = Car
    template_name = 'update_car.html'
    fields = ['license_plate', 'color']
    success_url = '/car/list/'


class DeleteCar(DeleteView):
    model = Car
    context_object_name = 'car'
    template_name = 'delete_car.html'
    success_url = '/car/list/'
