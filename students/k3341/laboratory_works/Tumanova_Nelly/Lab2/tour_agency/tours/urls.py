from django.urls import path

from . import views
from .apps import ToursConfig

app_name = ToursConfig.name
urlpatterns = [
    path('', views.TourListView.as_view(), name='available'),
    path('all/', views.StaffTourListView.as_view(), name='all'),
    path('add/', views.StaffTourCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TourDetailView.as_view(), name='detail'),
    path('upcoming/', views.ClientUpcomingTripsView.as_view(), name='upcoming'),
    path('history/', views.ClientHistoryView.as_view(), name='history'),
    path('departure/<int:pk>/', views.StaffDepartureDetailView.as_view(), name='departure'),
    path('departure/<int:pk>/reserve/', views.ReserveDepartureView.as_view(), name='reserve_departure'),
    path('departure/<int:pk>/cancel/', views.CancelReservationView.as_view(), name='cancel_reservation'),
    path('departure/', views.StaffDepartureListView.as_view(), name='departures'),

]