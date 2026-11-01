from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Flight, Airport
from .forms import FlightForm

class FlightListView(ListView):
    model = Flight
    template_name = 'flight_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().order_by('departure_time')

        search = self.request.GET.get('search')
        airport = self.request.GET.get('airport')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(flight_number__icontains=search)
        if airport:
            queryset = queryset.filter(departure_airport_id=airport)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airports'] = Airport.objects.all()
        return context

class FlightCreateView(CreateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightUpdateView(UpdateView):
    model = Flight
    form_class = FlightForm
    template_name = 'flight_form.html'
    success_url = reverse_lazy('flight_list')

class FlightDeleteView(DeleteView):
    model = Flight
    template_name = 'flight_confirm_delete.html'
    success_url = reverse_lazy('flight_list')