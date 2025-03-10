from django.shortcuts import render
from django.http import Http404
from .forms import *

from django.views.generic import *


def get_owner(request, car_owner_id):
    try:
        owner = CarOwner.objects.get(pk=car_owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")

    return render(request, "owner.html", {"owner": owner})


def list_owners(request):
    try:
        owners = CarOwner.objects.all()
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")

    return render(request, "owners.html", {"owners": owners})


class GetCarView(DetailView):
    model = Car
    template_name = "car.html"


class ListCarsView(ListView):
    model = Car
    template_name = "cars.html"


class UpdateCarView(UpdateView):
    model = Car
    fields = [
        'state_number',
        'mark',
        'model',
        'colour'
    ]
    template_name = 'car_updater.html'
    success_url = '/cars'


def create_owner(request):
    context = {}
    form = CreateOwnerForm(request.POST or None)

    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "owner_create.html", context)


class CreateCarView(CreateView):
    model = Car
    form_class = CreateCarForm
    template_name = "car_create.html"
    success_url = "/cars"


class UpdateCarFormView(UpdateView):
    model = Car
    form_class = UpdateCarForm
    template_name = "car_update_form.html"
    success_url = "/cars/"


class DeleteCarView(DeleteView):
    model = Car
    template_name = "car_delete.html"
    success_url = "/cars/"
