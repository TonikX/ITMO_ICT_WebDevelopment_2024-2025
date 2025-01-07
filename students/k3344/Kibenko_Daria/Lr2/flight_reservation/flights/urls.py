from django.urls import path
from .views import flight_list, my_reservations, reserve_flight

urlpatterns = [
    path('', flight_list, name='flight_list'),
    path('my_reservations/', my_reservations, name='my_reservations'),
    path('reserve/<str:flight_number>/', reserve_flight, name='reserve_flight'),
]
