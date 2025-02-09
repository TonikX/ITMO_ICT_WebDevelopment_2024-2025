from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from project_first_app.forms import AutoOwnerForm
from project_first_app.models import AutoOwner, Auto
def detail(request, owner_id):
    try:
        p = AutoOwner.objects.get(pk=owner_id)
    except AutoOwner.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'owner.html', {'owner': p})

def list_view(request):
    context = {}
    context["dataset"] = AutoOwner.objects.all()
    return render(request, "owner_list_views.html", context)

from django.views.generic.detail import DetailView

class AutoRetrieveView(DetailView):
  model = Auto

class AutoListView(ListView):
  model = Auto
  queryset = model.objects.all()

class AutoUpdateView(UpdateView):
  model = Auto
  fields = ['state_number', 'brand', 'model', 'color']
  success_url = '/auto/list/'


class AutoCreateView(CreateView):
  model = Auto
  fields = ['state_number', 'brand', 'model', 'color']
  success_url = '/auto/list/'


class AutoDeleteView(DeleteView):
  model = Auto
  success_url = '/auto/list/'


def create_view(request):
    context = {}

    form = AutoOwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, "create_auto_owner_view.html", context)