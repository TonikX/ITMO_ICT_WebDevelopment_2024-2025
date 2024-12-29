from django.urls import path 
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView, CreateCarOwnerView

urlpatterns = [
     path('owners/', views.owner_list, name='owner_list'),
     path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
     path('owner/add/', CreateCarOwnerView.as_view(), name='add_owner'),
     path('cars/', CarListView.as_view(), name='car_list'),
     path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
     path('car/add/', CarCreateView.as_view(), name='car_add'),
     path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
     path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),

]