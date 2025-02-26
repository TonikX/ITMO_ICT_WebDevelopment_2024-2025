from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CarForm, CarOwnerCreateForm
from .models import CarOwner, Car

def car_owner_detail(request, car_owner_pk):
    try:
        car_owner = CarOwner.objects.get(pk=car_owner_pk)
    except CarOwner.DoesNotExist:
        raise Http404("Владельца автомобиля не существует")

    context = {
        'car_owner': car_owner,
        'title': "Информация о водителе",
    }
    return render(request, 'owner/owner.html', context)

def all_car_owners(request):
    owners = CarOwner.objects.all()
    context = {
        'owners': owners,
        'title': "All Car Owners",
    }
    return render(request, 'owner/all_owners.html', context)

def car_owner_create(request):
    context = {}
    if request.method == 'POST':
        form = CarOwnerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_car_owners')
    else:
        form = CarOwnerCreateForm()
    context["form"] = form
    return render(request, "owner/owner_create.html", context)

class AllCarsView(ListView):
    model = Car
    template_name = 'owner/all_cars.html'
    context_object_name = "cars"
    extra_context = {'title': 'All cars'}

class CarDetailView(DetailView):
    model = Car
    template_name = 'owner/car_detail.html'
    context_object_name = "car"
    extra_context = {'title': 'Car detail'}

class CarUpdateView(UpdateView):
    model = Car
    fields = ['car_number', 'mark', 'model', 'colour']
    template_name = 'owner/car_update.html'
    success_url = '/cars/'

class CarCreateView(CreateView):
    model = Car
    template_name = 'owner/car_create.html'
    form_class = CarForm
    success_url = '/cars/'

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'owner/car_delete.html'
    success_url = '/cars/'
    pk_url_kwarg = 'pk'