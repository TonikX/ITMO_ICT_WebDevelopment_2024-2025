from django.urls import path
from . import views

urlpatterns = [
    # path('owners/list', views.owners_list, name='owners'),
    path('owners/<int:id>/', views.owner_by_id, name='owner'),
    path('owners/list/', views.OwnersListView.as_view(), name='owners'),
    path('owners/create/', views.OwnersCreateView.as_view(), name='owners_create'),
    path('owners/<int:pk>/delete/', views.OwnersDeleteView.as_view(), name='owners_delete'),
    # path('cars/', views.cars_list, name='cars'),
    path('cars/<int:id>/', views.car_by_id, name='car'),
    path('cars/list/', views.CarsListView.as_view(), name='cars'),
    path('cars/create/', views.CarCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='cars_delete'),
]
