from django.urls import path
from .views import (
    OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView,
    CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView
)

urlpatterns = [
    path('owners/', OwnerListView.as_view(), name='owner-list'),
    path('owners/create/', OwnerCreateView.as_view(), name='create_owner'),
    path('owners/<int:pk>/', OwnerDetailView.as_view(), name='owner_detail'),
    path('owners/<int:pk>/update/', OwnerUpdateView.as_view(), name='update_owner'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='delete_owner'),

    path('cars/', CarListView.as_view(), name='car-list'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car-update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car-delete'),
]
