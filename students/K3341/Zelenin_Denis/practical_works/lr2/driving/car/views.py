from django.shortcuts import render
from .models import Owner
from .models import  Car
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from  .forms import  OwnerForm
from django.views.generic.edit import UpdateView
from  django.views.generic.edit import DeleteView


def car_detail(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)  # Получить объект Car по его id
    return render(request, 'car/index.html', {'owner': owner})

def owners_list(request):
    context = {}
    context["dataset"] = Owner.objects.all()
    return render(request, 'car/list.html', context)

class CarListView(ListView):
    model = Car
    template_name = 'car/list_class.html'
    context_object_name = 'cars'

class CarDetail(DetailView):
    model = Car
    template_name = 'car/car_detail.html'
    context_object_name = 'car'


def OwnerCreateView(request):
    context = {}
    form = OwnerForm(request.POST or None)

    if form.is_valid():

        form.save()
    context['form'] = form
    return render(request, "car/OwnerCreateView.html", context)


class PublisherUpdateView(UpdateView):

    model = Car
    template_name = 'car/update_car.html'
    fields = ['state_number', 'brand', 'color', 'mark']
    success_url = '/car/list/'
class CarDelete(DeleteView):

    model = Car
    template_name = 'car/delete_car.html'
    success_url = '/car/list/'

