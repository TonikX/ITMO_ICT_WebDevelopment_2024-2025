from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import DeletionMixin

from project_first_app.forms import OwnerForm
from project_first_app.models import Owner, Car


def owner(request, owner_id):
    try:
        owner_model = Owner.objects.get(id=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner_model})


def owners(request):
    context = {"owners": Owner.objects.all()}

    return render(request, "owners.html", context)


def create_owner(request):
    context = {}
    form = OwnerForm(
        request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_owner.html", context)


class CarsList(ListView):
    model = Car
    context_object_name = 'cars'
    template_name = 'cars.html'


class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car.html'


class CarCreateView(CreateView):
    model = Car
    template_name = 'car_create.html'
    fields = '__all__'
    success_url = '/cars/'


class CarUpdateView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'car_delete.html'

