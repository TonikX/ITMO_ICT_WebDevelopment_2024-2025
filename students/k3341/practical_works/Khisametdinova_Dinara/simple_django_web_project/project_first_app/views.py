from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from project_first_app.forms import CreateCarForm, CreateOwnerForm, UpdateCarForm

from .models import CarOwner, Car


def owner_detail(request, id):
    try:
        owner = CarOwner.objects.get(pk=id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})

class CarOwnerListView(ListView):
    model = CarOwner
    template_name = 'carowner_list.html'
    context_object_name = 'owners'

class CarOwnerCreateView(CreateView):
    model = CarOwner
    form_class = CreateOwnerForm
    template_name = 'carowner_form.html'
    success_url = reverse_lazy('owner_list')

class CarOwnerUpdateView(UpdateView):
    model = CarOwner
    form_class = CreateOwnerForm
    template_name = 'carowner_form.html'
    success_url = reverse_lazy('owner_list')

class CarOwnerDeleteView(DeleteView):
    model = CarOwner
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('owner_list')

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarCreateView(CreateView):
    model = Car
    form_class = CreateCarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarUpdateView(UpdateView):
    model = Car
    form_class = UpdateCarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')
