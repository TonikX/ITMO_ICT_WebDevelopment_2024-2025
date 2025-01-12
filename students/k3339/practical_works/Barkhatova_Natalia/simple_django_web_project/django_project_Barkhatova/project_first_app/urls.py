from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.detail, name='owner_detail'),
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/add/', views.add_owner, name='add_owner'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('register/', views.register, name='register'),
    path('create_owner/', views.create_owner, name='create_owner'),
]
