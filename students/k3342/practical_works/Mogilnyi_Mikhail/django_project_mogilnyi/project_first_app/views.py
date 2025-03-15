from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView,  CreateView, DeleteView
from django.http import Http404
from django.shortcuts import render
from .models import CarOwner, Car
from django import forms

def home(request):
    return render(request, 'home.html')
def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})

def owners_list(request):
    context = {
        "owners": CarOwner.objects.all()
    }
    return render(request, "owners_list.html", context)

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate', 'make', 'model', 'color']
    template_name = 'car_update.html'
    success_url = reverse_lazy('car_list')


class OwnerForm(forms.ModelForm):
    class Meta:
        model = CarOwner
        fields = ['first_name', 'last_name', 'birth_date']


def create_owner_view(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'create_owner.html', {'form': form})

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['license_plate', 'make', 'model', 'color']

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('cars_list')

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('cars_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('cars_list')

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})