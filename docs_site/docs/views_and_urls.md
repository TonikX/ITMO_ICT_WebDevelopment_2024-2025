# View и urls.py

## 🔹 Основная логика

Реализованы классы и функции:
- `HotelDetailView` — страница отеля с номерами  
- `booking_create` — создание бронирования  
- `UserBookingsListView` — список личных бронирований  
- `booking_edit` / `booking_delete` — редактирование и удаление брони  
- `RecentGuestsListView` — постояльцы за последний месяц  
- `add_review` — добавление отзывов

## 🔹 Страничка отеля с номерами 

```python
class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = self.object.rooms.all()
        return context
```

## 🔹 Создание бронирования

```python
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'hotels/booking_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'room': self.get_room()}
        return kwargs

    def get_room(self):
        from .models import Room
        return Room.objects.get(pk=self.kwargs['room_id'])

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room = self.get_room()
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('hotels:user_bookings')
```

## 🔹 Последние посетители

```python
class RecentGuestsListView(ListView):
    model = Booking
    template_name = 'hotels/recent_guests.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        since = date.today() - timedelta(days=30)
        return Booking.objects.filter(check_out__gte=since, check_in__lte=date.today()).select_related('user', 'room')
```

##🔹 urls.py
```python
urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('booking/create/<int:room_id>/', views.booking_create, name='booking_create'),
    path('booking/delete/<int:pk>/', views.booking_delete, name='booking_delete'),
    path('booking/edit/<int:pk>/', views.booking_edit, name='booking_edit'),
    path('bookings/', views.UserBookingsListView.as_view(), name='user_bookings'),
    path('recent_guests/', views.RecentGuestsListView.as_view(), name='recent_guests'),
    path('review/<int:room_id>/add/', views.add_review, name='add_review'),
]
```