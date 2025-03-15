from django.shortcuts import render
from django.http import Http404 
from blog.models import Owner, Car
from .forms import OwnerForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.
def detail(request, owner_id):
    try:
        owner_model = Owner.objects.get(id=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner_model}) 

def owner_list(request):
    context = {"dataset": Owner.objects.all()}
    return render(request, "owner_list_view.html", context)


def create_owner_view(request):
    context = {}
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_owner_view.html", context)


class CarList(ListView):
    model = Car
    template_name = 'car_list_view.html'


class CarRetrieveView(DetailView):
    model = Car
    template_name = 'car_details.html'


class CarCreateView(CreateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'
    template_name = 'car_create.html'


class CarUpdateView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'
    template_name = 'car_update.html'


class CarDeleteView(DeleteView):
    model = Car
    success_url = '/cars/'
    template_name = 'car_delete.html'