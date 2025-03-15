from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from .models import Owner, Car
from .forms import OwnerForm, CarForm

def owners(request):
    owners = Owner.objects.all()
    return render(request, 'owner.html', {'owners': owners})

def detail(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})


def add_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/owner/')
    else:
        form = OwnerForm()
    return render(request, 'owner_form.html', {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['state_number', 'brand', 'model', 'colour']
    template_name = 'car_data.html'
    success_url = '/cars/'


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_type.html'
    success_url = reverse_lazy('cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить автомобиль'
        context['button_text'] = 'Добавить'
        return context


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_type.html'
    success_url = reverse_lazy('cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновить автомобиль'
        context['button_text'] = 'Сохранить изменения'
        return context


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = reverse_lazy('cars')
