from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import CarOwner, Car
from .forms import CarOwnerForm, CarForm


def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner_detail.html', {'owner': owner})


def owner_list(request):
    try:
        owners = CarOwner.objects.all()
    except CarOwner.DoesNotExist:
        raise Http404("Owners do not exist")
    return render(request, 'owners_list.html', {'owners': owners})


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


def create_owner(request):
    if request.method == "POST":
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/owners")
    else:
        form = CarOwnerForm()

    return render(request, 'owner_create.html', {'form': form})


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_create.html'
    context_object_name = 'form'
    success_url = '/cars/'


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'
    context_object_name = 'form'
    success_url = '/cars/'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    context_object_name = 'car'
    success_url = '/cars/'
