from django.shortcuts import render
from django.http import Http404
from django.urls import reverse_lazy

from .models import Owner
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Auto
from django.shortcuts import render, redirect
from .forms import CarOwnerForm, CarForm


def add_owner(request):
   if request.method == 'POST':
       form = CarOwnerForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('owner_list')
   else:
       form = CarOwnerForm()


   return render(request, 'add_owner.html', {'form': form})

class CarListView(ListView):
   model = Auto
   template_name = 'car_list.html'

class CarDetailView(DetailView):
   model = Auto
   template_name = 'car_detail.html'

class CarCreateView(CreateView):
   model = Auto
   form_class = CarForm
   template_name = 'car_form.html'
   success_url = reverse_lazy('car_list')




class CarUpdateView(UpdateView):
   model = Auto
   form_class = CarForm
   template_name = 'car_form.html'
   success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
   model = Auto
   template_name = 'car_confirm_delete.html'
   success_url = reverse_lazy('car_list')


# Create your views here.
def owner_detail(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("CarOwner does not exist")
    return render(request, 'owner.html', {'owner': owner})

def owner_list_view(request):
   owners = Owner.objects.all()
   return render(request, 'owner_list.html', {'owners': owners})
