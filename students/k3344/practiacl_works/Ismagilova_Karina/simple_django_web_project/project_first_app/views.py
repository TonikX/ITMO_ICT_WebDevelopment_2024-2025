from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, ListView
from .models import Owner, Car
from .forms import OwnerForm, CarForm

def detail(request, owner_id):
    try:
        p = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': p})

def owners_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner.html', {'owners': owners})

def new_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('owners_list'))
    else:
        form = OwnerForm()
    return render(request, 'new_owner.html', {'form': form})

class OwnerDeleteView(DeleteView):
    model = Owner
    template_name = 'owner_delete.html'
    success_url = '/owners/'

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
    fields = ['car_number', 'car_brand', 'car_model', 'colour']
    template_name = 'car_update.html'
    success_url = '/cars/'

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_update.html'
    success_url = '/cars/'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'
