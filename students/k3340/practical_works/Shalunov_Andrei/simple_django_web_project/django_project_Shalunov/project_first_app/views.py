from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner, Car
from .forms import OwnerForm, CarForm


class OwnerListView(ListView):
    model = Owner
    template_name = 'owners_list.html'
    context_object_name = 'owners'


class OwnerDetailView(DetailView):
    model = Owner
    template_name = 'owner_detail.html'
    context_object_name = 'owner'


class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerForm
    template_name = 'owner_form.html'
    success_url = reverse_lazy('owners_list')


class OwnerUpdateView(UpdateView):
    model = Owner
    fields = ['first_name', 'last_name', 'birthday_date', 'passport_number', 'home_address', 'nationality']
    template_name = 'owner_form.html'
    success_url = reverse_lazy('owners_list')


class OwnerDeleteView(DeleteView):
    model = Owner
    template_name = 'owner_delete.html'
    success_url = reverse_lazy('owners_list')


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
    template_name = 'car_delete.html'
    success_url = reverse_lazy('car_list')
