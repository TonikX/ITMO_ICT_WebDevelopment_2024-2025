from django.shortcuts import render, redirect
from django.http import Http404 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.urls import reverse

from .models import User, Car


def owner_info(request, id):
    try:
        owner = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404("Owner does not exist")
    
    context = {'owner': owner}
    return render(request, 'project_first_app/owner_info_view.html', context)


def owners(request):
    owners_list = User.objects.all()
    context = {'owners': owners_list}
    return render(request, 'project_first_app/owners_list_view.html', context)


def create_owner(request):
    context = {}

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('owners'))
    
    else:
        form = UserForm()
        context['form'] = form

    return render(request, 'project_first_app/owner_create_view.html', context)


class CarsListView(ListView):
    model = Car
    template_name = 'project_first_app/cars_list_view.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    context_object_name = 'car'
    template_name = 'project_first_app/car_detail_view.html'


class CreateCarView(CreateView):
    model = Car
    template_name = 'project_first_app/car_create_view.html'
    success_url='/cars/'
    fields = ['state_number', 'brand', 'model', 'color']


class UpdateCarView(UpdateView):
    model = Car
    template_name = 'project_first_app/car_update_view.html'
    success_url='/cars/'
    fields = ['state_number', 'brand', 'model', 'color']


class DeleteCarView(DeleteView):
    model = Car
    template_name = 'project_first_app/car_delete_view.html'
    success_url='/cars/'
