from django.urls import path
from .views import FlightListView, FlightCreateView, FlightUpdateView, FlightDeleteView

urlpatterns = [
    path('', FlightListView.as_view(), name='flight_list'),
    path('create/', FlightCreateView.as_view(), name='flight_create'),
    path('<int:pk>/update/', FlightUpdateView.as_view(), name='flight_update'),
    path('<int:pk>/delete/', FlightDeleteView.as_view(), name='flight_delete'),
]