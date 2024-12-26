from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from project_first_app.forms import OwnerForm
from project_first_app.models import Owner, Car


def get_owner(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, "get_owner.html", {"owner": owner})


def get_owners(request):
    owners = Owner.objects.all()
    return render(request, "get_owners.html", {"owners": owners})


def create_owner(request):
    context = {}
    form = OwnerForm(
        request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_owner.html", context)


class GetCarView(DetailView):
    model = Car
    template_name = "get_car.html"
    context_object_name = 'car'


class GetCarsView(ListView):
    model = Car
    template_name = "get_cars.html"
    context_object_name = 'cars'


class CreateCarView(CreateView):
    model = Car
    fields = ['license_plate', 'brand', 'model', 'color']
    template_name = 'create_car.html'
    success_url = '/get_cars'


class UpdateCarView(UpdateView):
    model = Car
    fields = ['license_plate', 'brand', 'model', 'color']
    template_name = 'update_car.html'
    success_url = '/get_cars'


class DeleteCarView(DeleteView):
    model = Car
    template_name = 'delete_car.html'
    success_url = '/get_cars'
