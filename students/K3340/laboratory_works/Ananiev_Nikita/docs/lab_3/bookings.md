## Приложение booking_api.
### Назначение: отвечает за запросы связанные с бронированием номеров.

### models.py:
```python
from django.db import models
from django.utils import timezone

from hotel_api.models import Room
from auth_api.models import UserAccount

class Booking(models.Model):
    booking_date = models.DateField(null=False, default=timezone.now)
    from_town = models.CharField(max_length=30)
    check_in_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    full_days = models.IntegerField(default=0)
    state = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30)
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, related_name='bookings')

    def __str__(self):
        return f"Booking from {self.booking_date} by {self.client.firstname} {self.client.lastname}, room {self.room.number}"
```

### serializers.py:
```python
from rest_framework import serializers
from .models import Booking
from hotel_api.serializers import RoomSerializer
from auth_api.serializers import CustomUserSerializer


class BookingDetailedSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer()
    room = RoomSerializer()
    class Meta:
        model = Booking
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['client', 'room', 'booking_date', 'from_town']

    def create(self, validated_data):
        booking = Booking(**validated_data)
        booking.payment_status = 'not paid'
        booking.state = 'booked'
        booking.save()
        return Booking(**validated_data)


class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in_time', 'departure_time', 'full_days', 'state', 'payment_status']
        depth = 1
```

### urls.py:
```python
urlpatterns = [
    path('bookings/<int:id>/', BookingAPIView.as_view(), name='get_booking'),
    path('bookings/list/', BookingListAPIView.as_view(), name='get_booking_list'),
    path('bookings/add/', BookingCreateAPIView.as_view(), name='add_booking'),
    path('bookings/<int:id>/update/', BookingUpdateAPIView.as_view(), name='update_booking'),
    path('bookings/<int:id>/delete/', BookingDeleteAPIView.as_view(), name='delete_booking'),
]
```