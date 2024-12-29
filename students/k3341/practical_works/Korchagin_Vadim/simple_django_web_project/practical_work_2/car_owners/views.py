from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from car_owners.forms import CarOwnerForm, CarForm
from car_owners.models import CarOwner, Car, Ownership, DriverLicense

def owner_detail(request, owner_id):
    owner = CarOwner.objects.get(id=owner_id)  
    return render(request, 'owner.html', {'owner': owner})

def owner_list(request):
    owners = CarOwner.objects.all()
    return render(request, 'owners_list.html', {'owners': owners})

def add_owner(request):
    if request.method == 'POST':
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = CarOwnerForm()
    return render(request, 'add_owner.html', {'form': form})
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
    success_url = '/cars/'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/cars/'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = '/cars/'