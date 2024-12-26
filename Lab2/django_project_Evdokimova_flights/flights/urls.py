from django.urls import path
from . import views
from django.urls import path
from flights import views
from flights.views import flight_list
from flights.views import flight_detail, create_review, create_reservation


urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('flight/<int:flight_id>/review/', views.create_review, name='create_review'),
]
