from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import Http404
from django.shortcuts import render

from .forms import *
from .models import *


def car_owner_detail(request, car_owner_id):
    print(f"Получен ID владельца: {car_owner_id}")
    try:
        car_owner = Car_owner.objects.get(pk=car_owner_id)
    except Car_owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'car_owner.html', {'car_owner': car_owner})

def owner_list(request):
    owners = Car_owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

def create_owner_view(request):
    context ={}

    form = OwnerForm(request.POST or None)
    if form.is_valid(): 
        form.save()
    context['form'] = form
    return render(request, "owner_form.html", context)

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/cars'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'
    success_url = '/cars'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars'

