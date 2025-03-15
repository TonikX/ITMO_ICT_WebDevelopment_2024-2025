from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import DeletionMixin

from .models import Car

from .forms import OwnerForm
from .models import Owner


class ListOfCars(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'car/cars.html'


class RetrieveCarView(DetailView):
    model = Car
    template_name = 'car/cars.html'


class CreateCarView(CreateView):
    model = Car
    template_name = 'car/car_create.html'
    fields = '__all__'
    success_url = '/cars/'


class UpdateCarView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'


class DeleteCarView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'car/car_delete.html'


class DeleteListOfCarsView(DeletionMixin):
    model = Car
    success_url = '/cars/'
    template_name = 'car/cars_delete.html'

def get_owner(request, owner_id):
    try:
        owner_model = Owner.objects.get(id=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner/owner.html', {'owner': owner_model})


def get_all_owners(request):
    context = {"owners": Owner.objects.all()}
    return render(request, "owner/owners.html", context)


def create_owner(request):
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "owner/create_owner.html", context)