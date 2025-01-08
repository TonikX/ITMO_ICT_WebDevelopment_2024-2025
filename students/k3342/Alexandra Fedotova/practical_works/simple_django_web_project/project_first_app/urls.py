from django.urls import path
from . import views
from .views import CarListView, CarCreateView, CarDetailView, CarUpdateView, CarDeleteView
from .views import add_and_list_car_owners

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owners/', add_and_list_car_owners, name='car_owners'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/add/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/edit/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]