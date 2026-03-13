from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('guests/last-month/', views.GuestsLastMonthView.as_view(), name='guests_last_month'),
]