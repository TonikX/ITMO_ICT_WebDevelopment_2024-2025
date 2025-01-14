from django.shortcuts import render, redirect
from django.http import Http404
from .models import CarOwner, Car
from .form import CarOwnerForm, CarForm, CarDeleteForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView


def get_owner(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Car owner does not exist")
    return render(request, 'owner.html', {'owner': owner})


def get_all_owners(request):
    try:
        all_owners = CarOwner.objects.all()
    except CarOwner.DoesNotExist:
        raise Http404("Empty table")
    return render(request, 'all_owners.html', {'all_owners': all_owners})


def create_owner_form(request):
    context = {}
    form = CarOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('get_all_owners')
    context['form'] = form
    return render(request, "create_owner.html", context)


class CarsListView(ListView):
    model = Car
    template_name = 'all_cars.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car.html'
    context_object_name = 'car'


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'update_car.html'
    fields = ["brand", "model", "color", "gos_number"]
    context_object_name = 'update_car'
    success_url = '/cars'


class CarCreateView(CreateView):
    model = Car
    form = CarForm
    fields = ["brand", "model", "color", "gos_number"]
    template_name = 'create_car.html'
    success_url = '/cars'


class CarDeleteView(FormView):
    template_name = 'delete_car.html'
    form_class = CarDeleteForm
    success_url = '/cars'

    def form_valid(self, form):
        car = form.cleaned_data['car']
        car.delete()
        return redirect(self.success_url)
