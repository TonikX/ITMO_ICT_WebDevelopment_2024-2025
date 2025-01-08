from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotel_list', views.hotel_list, name='hotel_list'),
    path('<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
]