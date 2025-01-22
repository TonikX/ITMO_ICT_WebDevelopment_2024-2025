from django.urls import path

from . import views  # Импортируем контроллеры из views.py

urlpatterns = [
    path('car_owner/<int:car_id>/', views.car_owner_details, name='car_owner_details'),
]
