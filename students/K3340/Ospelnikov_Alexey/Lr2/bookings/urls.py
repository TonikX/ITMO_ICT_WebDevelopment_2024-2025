from django.urls import path
from . import views

urlpatterns = [
  path('list/', views.booking_list, name='booking_list'),
  path('edit/<int:pk>/', views.booking_edit, name='booking_edit'),
  path('delete/<int:pk>/', views.booking_delete, name='booking_delete'),
   path('guests/', views.current_guests, name='current_guests'),
]