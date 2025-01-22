from django.http import Http404
from django.shortcuts import render
from project_first_app.models import Driver
from .models import Car
from .form import DriverForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView


def driver(request, driver_id):
    try:
        p = Driver.objects.get(pk=driver_id)
    except Driver.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'driver.html', {'driver': p})


def alldrivers(request):
    visual = {"drivers": Driver.objects.all()}
    return render(request, 'alldrivers.html', visual)


class carView(DetailView):
    model = Car
    template_name = 'car.html'


def allcars(request):
    visual = {"cars": Car.objects.all()}
    return render(request, 'allcars.html', visual)


class updatecarView(UpdateView):
    model = Car
    fields = ['id', 'label', 'model', 'color', 'use']
    success_url = '/allcars/'
    template_name = 'updatecar.html'


def createdriverView(request):
    visual = {}
    form = DriverForm(request.POST or None)
    if form.is_valid():
        form.save()
    visual['form'] = form
    return render(request, 'createdriver.html', visual)


class createcar(CreateView):
    model = Car
    template_name = 'createcar.html'
    fields = ['id', 'label', 'model', 'color', 'use']
    success_url = '/allcars/'


class deletecarView(DeleteView):
    model = Car
    success_url = '/allcars/'
    template_name = 'deletecar.html'