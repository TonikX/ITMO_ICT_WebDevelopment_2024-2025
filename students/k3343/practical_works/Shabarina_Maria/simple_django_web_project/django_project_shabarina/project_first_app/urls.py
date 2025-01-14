from django.urls import path
from . import views
from .views import CarsListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView


urlpatterns = [
     path('owner/<int:owner_id>/', views.get_owner, name='get_owner'),
     path('owners/', views.get_all_owners, name='get_all_owners'),
     path('cars/', CarsListView.as_view(), name='all_cars'),
     path('car/<int:pk>/', CarDetailView.as_view(), name='car'),
     path('update_car/<int:pk>/', CarUpdateView.as_view(), name='update_car'),
     path('create_owner/', views.create_owner_form, name='create_owner'),
     path('create_car/', CarCreateView.as_view(), name='create_car'),
     path('delete_car/', CarDeleteView.as_view(), name='delete_car'),
]