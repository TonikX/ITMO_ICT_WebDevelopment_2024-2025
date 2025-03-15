from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import *


def detail(request, car_owner_id):
    try:
        owner = CarOwner.objects.get(pk=car_owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")

    return render(request, 'detail.html', {'owner': owner})


def owners(request):
    owners = CarOwner.objects.all()
    return render(request, 'owners.html', {'owners': owners})


class CarList(ListView):
    model = Car
    template_name = 'cars_list.html'


class CarDetail(DetailView):
    model = Car
    template_name = 'car_detail.html'


def create_owner(request):
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = f"{user.first_name}{user.last_name}"
        user.save()
        return redirect("owners")
    context['form'] = form
    return render(request, 'create_owner.html', context)


class CarUpdateView(UpdateView):
    model = Car
    fields = ['number', 'label', 'model', 'color']
    success_url = '/car/list/'
    template_name = 'car_edit.html'


class CarCreate(CreateView):
    model = Car
    template_name = 'create_car.html'
    fields = ['number', 'label', 'model', 'color']
    success_url = '/car/list/'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/car/list/'
    template_name = 'car_delete.html'


def index(request):
    return render(request, 'index.html')
