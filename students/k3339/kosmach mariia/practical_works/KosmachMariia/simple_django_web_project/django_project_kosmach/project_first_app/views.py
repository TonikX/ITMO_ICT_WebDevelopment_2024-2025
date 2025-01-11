from django.shortcuts import render
from project_first_app.models import *
from project_first_app.forms import *
from django.views.generic import *


def get_owner(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner not found.")

    return render(request, "get_owner.html", {"owner": owner})


def get_owners(request):
    owners = Owner.objects.all()
    return render(request, "get_owners.html", {"owners": owners})


class GetCarsView(ListView):
    model = Car
    template_name = "get_cars.html"


class GetCarView(DetailView):
    model = Car
    template_name = "get_car.html"


class UpdateCarView(UpdateView):
    model = Car
    fields = ['number', 'brand', 'model', 'color']
    template_name = 'update_car.html'
    success_url = '/get_cars'


def create_owner(request):
    context = {}
    form = CreateOwnerForm(
        request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_owner.html", context)


class CreateCarView(CreateView):
    model = Car
    form_class = CreateCarForm
    template_name = "create_car.html"
    success_url = "/get_cars"


class UpdateCarFormView(UpdateView):
    model = Car
    form_class = UpdateCarForm
    template_name = "update_car_form.html"
    success_url = "/get_cars"


class DeleteCarView(DeleteView):
    model = Car
    template_name = "delete_car.html"
    success_url = "/get_cars"
