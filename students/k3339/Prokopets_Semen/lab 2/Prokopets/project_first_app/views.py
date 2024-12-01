from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CarForm, OwnerForm
from django.http import Http404, HttpResponse
from project_first_app.models import Car
from project_first_app.models import DriveLicense
from project_first_app.models import Owner
from project_first_app.models import Possession
import datetime

def cars(request, car_id):
    try:
        p = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        raise Http404(
            "Car does not exist")
    return render(request, 'car.html', {'car': p})


def possessions(request, possession_id):
    try:
        p = Possession.objects.get(pk=possession_id)
    except Possession.DoesNotExist:
        raise Http404(
            "Possession does not exist")
    return render(request, 'possession.html', {'possession': p})

def owners_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

def owners(request, owner_id):
    try:
        p = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404(
            "Owner does not exist")
    return render(request, 'owner.html', {'owner': p})


def driveLicenses(request, driveLicense_id):
    try:
        p = DriveLicense.objects.get(pk=driveLicense_id)
    except DriveLicense.DoesNotExist:
        raise Http404(
            "DriveLicense does not exist")
    return render(request, 'driveLicense.html', {'driveLicense': p})


class CarListView(View):
    def get(self, request):
        cars = Car.objects.all()
        return render(request, 'car/car_list.html', {'cars': cars})

class CarDetailView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        return render(request, 'cars/car_detail.html', {'car': car})

class CarUpdateView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarForm(instance=car)
        return render(request, 'Car/car_form.html', {'form': form})

    def post(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()  # Сохраняем обновленные данные
            return redirect('car_detail', car_id=car.id)
        return render(request, 'car/car_form.html', {'form': form})

# create a function
def example_view(request):
    # fetch date and time
    now = datetime.datetime.now()
    # convert to string
    html = "Time is {}".format(now)
    # return response
    return HttpResponse(html)

def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owner/owner_form.html', {'form': form})