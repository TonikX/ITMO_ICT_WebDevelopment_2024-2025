from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import CarOwner, Car


class CarListView(ListView):
    model = Car
    template_name = 'cars_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        brand = self.request.GET.get('brand')
        if brand:
            return self.model.objects.all().filter(brand=brand)
        return self.model.objects.all()


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_details.html'
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
    template_name = 'car_delete.html'
    success_url = '/car/list'


class CarOwnerDetailView(DetailView):
    model = CarOwner
    template_name = 'owner_details.html'
    context_object_name = 'owner'


class CarOwnerListView(ListView):
    model = CarOwner
    template_name = 'owners_list.html'
    context_object_name = 'owners'

    def get_queryset(self):
        first_name = self.request.GET.get('first_name')
        last_name = self.request.GET.get('last_name')
        if last_name:
            if first_name:
                return self.model.objects.all().filter(first_name=first_name, last_name=last_name)
            return self.model.objects.all().filter(last_name=last_name)
        if first_name:
            return self.model.objects.all().filter(first_name=first_name)
        return self.model.objects.all()


class CarOwnerCreateView(CreateView):
    model = CarOwner
    fields = ['last_name', 'first_name', 'birth_date']
    template_name = 'owner_form.html'
    success_url = '/owner/list'


class CarOwnerDeleteView(DeleteView):
    model = CarOwner
    template_name = 'owner_delete.html'
    success_url = '/owner/list'


class CarOwnerUpdateView(UpdateView):
    model = CarOwner
    fields = ['last_name', 'first_name', 'birth_date']
    template_name = 'owner_form.html'
    success_url = '/owner/list'
