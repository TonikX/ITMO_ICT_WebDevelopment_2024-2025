from django.shortcuts import render
from django.http import Http404
from project_first_app.models import carOwner, car
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from .form import OwnerForm




def get_carOwner(request, carOwner_id):
    try:
        owner = carOwner.objects.get(pk=carOwner_id)
    except carOwner.DoesNotExist:
        raise Http404("carOwner does not exist")

    return render(request, 'show_carOwner.html', {'carOwner': owner})

def carOwners(request):
    visual = {"carOwners": carOwner.objects.all()}
    return render(request, 'carOwners.html', visual)

def create_owner_view(request):
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_owner.html", context)

class CarView(DetailView):
    model = car
    template_name = 'car.html'


def cars(request):
    visual = {"cars": car.objects.all()}
    return render(request, 'cars.html', visual)


class CreateCar(CreateView):
    model = car
    template_name = 'create_car.html'
    fields = ['id', 'state_number', 'brand', 'model', 'color']
    success_url = '/cars/'


class UpdateCarView(UpdateView):
    model = car
    fields = ['id', 'state_number', 'brand', 'model', 'color']
    success_url = '/cars/'
    template_name = 'update_car.html'


class DeleteCarView(DeleteView):
    model = car
    success_url = '/cars/'
    template_name = 'delete_car.html'
