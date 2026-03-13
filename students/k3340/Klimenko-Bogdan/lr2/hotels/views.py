from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from .models import Hotel  # импортируем только Hotel из текущего приложения
from bookings.models import Booking  # Booking из приложения bookings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def index(request):
    """Главная страница со списком отелей"""
    hotels = Hotel.objects.all()
    return render(request, 'hotels/index.html', {'hotels': hotels})

class HotelDetailView(DetailView):
    """Детальная страница отеля с его номерами"""
    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'

class GuestsLastMonthView(TemplateView):
    """Отчёт о постояльцах за последний месяц"""
    template_name = 'hotels/guests_last_month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_ago = timezone.now() - timedelta(days=30)
        guests = Booking.objects.filter(
            Q(is_checked_in=True) & Q(check_in__gte=month_ago)
        ).select_related('user', 'room__hotel')
        context['guests'] = guests
        return context