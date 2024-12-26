from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import OwnerForm, CarForm
from .models import Owner, Car

def owner(request, owner_id):
    try:
        o = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'owner.html', {'owner': o})

def owners(request):
    return render(request, 'owners.html', {'owners': Owner.objects.all()})

def create_owner(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "owner_create.html", {'form': form})

class CarsList(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'cars.html'

class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car.html'
    pk_url_kwarg = "car_id"

class CarCreateView(CreateView):
    model = Car
    template_name = 'car_create.html'
    fields = '__all__'
    success_url = '/cars/'

class CarUpdateView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'
    template_name = 'car_update.html'
    pk_url_kwarg = "car_id"

class CarDeleteView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'car_delete.html'
    pk_url_kwarg = "car_id"
