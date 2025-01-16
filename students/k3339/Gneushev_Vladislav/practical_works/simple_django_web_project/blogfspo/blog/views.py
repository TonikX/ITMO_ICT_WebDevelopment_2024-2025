from django.http import Http404
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from .models import CarOwner, Car, Ownership, DriverLicense
from .forms import CarOwnerForm, CarForm


def get_owner_details(request, owner_id):
    try: 
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})


def get_owners(request):
    context = {"owners": CarOwner.objects.all()}
    return render(request, "owners.html", context)


def get_car_details(request, car_id):
    try: 
        car = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        raise Http404("Car does not exist")
    return render(request, 'car.html', {'car': car})


class CarsList(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'cars.html'


class UpdateCarView(UpdateView):
    model = Car
    fields = "__all__"
    success_url = "/cars/"
    template_name = "update_car.html"


def create_owner(request):
    context = {}
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context["form"] = form
    return render (request, "create_owner.html", context)


class CreateCarView(CreateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'
    template_name = 'create_car.html'


class UpdateCarView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'
    template_name = 'update_car.html'


class DeleteCarView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'delete_car.html'