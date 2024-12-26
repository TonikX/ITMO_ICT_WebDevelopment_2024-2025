from django.urls import path
from . import views
from .views import CarListView,OwnerDeleteView, CarDetailView, CarUpdateView, new_owner, CarCreateView, CarDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.detail, name='owner_detail'),
    path('owners/', views.owners_list, name='owners_list'),
    path('owners/add/', new_owner, name='add_owner'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update')
]
