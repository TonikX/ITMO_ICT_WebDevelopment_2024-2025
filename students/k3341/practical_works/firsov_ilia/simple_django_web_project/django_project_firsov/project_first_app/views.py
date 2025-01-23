from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, ListView, DetailView, UpdateView, DeleteView
)
from .forms import CarForm, CustomUserCreationForm
from .models import Car, CarOwner, DrivingLicense


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("owner_list")
    template_name = "registration/register.html"


class OwnerListView(ListView):
    model = CarOwner
    template_name = 'owner_list.html'
    context_object_name = 'owners'


class DrivingLicenseListView(ListView):
    model = DrivingLicense
    template_name = 'driving_license_list.html'
    context_object_name = 'licenses'


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class CarCreateView(CreateView):
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')


class OwnerDetailView(DetailView):
    model = CarOwner
    template_name = 'owner_detail.html'
    context_object_name = 'owner'
