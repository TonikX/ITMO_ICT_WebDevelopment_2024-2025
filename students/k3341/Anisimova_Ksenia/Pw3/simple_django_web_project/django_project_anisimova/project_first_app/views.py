from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import CarOwner, Car
import datetime

def car_owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'owner.html', {'owner': owner})

def example_view(request):
    # fetch date and time
    now = datetime.datetime.now()
    # convert to string
    html = "Time is {}".format(now)
    # return response
    return HttpResponse(html)

class CarListView(ListView):
    model = Car
    template_name = 'list_of_cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        brand = self.request.GET.get('brand')

        if brand:

            try:
                queryset = self.model.objects.all().filter(brand=brand)

            except ValueError:
                queryset = self.model.objects.none()

            return queryset

        return self.model.objects.all()


class CarDetailView(DetailView):
    model = Car
    template_name = 'details_of_car.html'
    context_object_name = 'car'


class CarCreateView(CreateView):
    model = Car
    fields = ['brand', 'model', 'license_plate', 'color']
    template_name = 'car_form.html'
    success_url = '/car/list'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['brand', 'model', 'license_plate', 'color']
    template_name = 'car_form.html'
    success_url = '/car/list'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete_confirm.html'
    success_url = '/car/list'


class CarOwnerListView(ListView):
    model = CarOwner
    template_name = 'list_of_owners.html'
    context_object_name = 'owners'

    def get_queryset(self):
        last_name = self.request.GET.get('last_name')
        if last_name:

            try:
                queryset = self.model.objects.all().filter(last_name=last_name)
            except ValueError:
                queryset = self.model.objects.none()

            return queryset

        return self.model.objects.all()


class CarOwnerDetailView(DetailView):
    model = CarOwner
    template_name = 'details_of_owner.html'
    context_object_name = 'owner'



class CarOwnerCreateView(CreateView):
    model = CarOwner
    fields = ['last_name', 'first_name', 'birth_date']
    template_name = 'owner_form.html'
    success_url = '/owner/list'


class CarOwnerUpdateView(UpdateView):
    model = CarOwner
    fields = ['last_name', 'first_name', 'birth_date']
    template_name = 'owner_form.html'
    success_url = '/owner/list'


class CarOwnerDeleteView(DeleteView):
    model = CarOwner
    template_name = 'owner_delete_confirm.html'
    success_url = '/owner/list'
