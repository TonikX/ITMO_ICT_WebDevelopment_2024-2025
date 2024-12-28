from django.shortcuts import render
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import Owner, Car
from .forms import OwnerForm

def owner(request, pk):
  try:
    x = Owner.objects.get(pk=pk)
  except Owner.DoesNotExist:
    raise Http404("Owner does not exist")
  return render(request, 'owner.html', {'owner': x})

def owners(request):
  try:
    x = Owner.objects.all()
  except Owner.DoesNotExist:
    raise Http404("Owner does not exist")
  return render(request, 'owners.html', {'owners': x})

class CarList(ListView):
  model = Car
  template_name = 'cars.html'

class CarDetail(DetailView):
  model = Car
  template_name = 'car.html'

def owner_create(request):
  form = OwnerForm(request.POST or None)
  if form.is_valid():
    form.save()
  return render(request, "owner_create.html", {'form': form})

class CarUpdate(UpdateView):
  model = Car
  fields = '__all__'
  template_name = 'car_update.html'
  success_url = '/car/'

class CarCreate(CreateView):
  model = Car
  fields = '__all__'
  template_name = 'car_create.html'
  success_url = '/car/'

class CarDelete(DeleteView):
  model = Car
  template_name = 'car_delete.html'
  success_url = '/car/'