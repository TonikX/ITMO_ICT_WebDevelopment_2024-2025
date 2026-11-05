from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView
from django.shortcuts import render

from .models import *


# Create your views here.
def owner_details(request, owner_id):
    owner = None
    error = None
    cars = []
    licenses = []

    try:
        owner = CarOwner.objects.get(id=owner_id)

        # end_date пустой = владеет сейчас
        current_ownerships = Ownership.objects.filter(
            owner=owner,
            end_date__isnull=True
        ).select_related('car')
        cars = [o.car for o in current_ownerships]

        licenses = License.objects.filter(owner=owner)

    except CarOwner.DoesNotExist:
        error = f"Владелец с ID {owner_id} не найден."
    except ValueError:
        error = "ID должен быть числом."

    return render(request, 'owners/owner.html', {
        'owner_id': owner_id,
        'owner': owner,
        'cars': cars,
        'licenses': licenses,
        'error': error,
    })


def owners(request):
    return render(request, 'owners/owners.html', {
        'owners': CarOwner.objects.filter()
    })


class CarListView(ListView):
    model = Car
    template_name = 'cars/cars.html'
    context_object_name = 'cars'
    ordering = ['make', 'model']


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ownerships'] = Ownership.objects.filter(
            car=self.object
        ).select_related('owner').order_by('-start_date')

        return context


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'cars/car_edit.html'
    fields = ['number_plate', 'make', 'model', 'color']
    success_url = reverse_lazy('car')