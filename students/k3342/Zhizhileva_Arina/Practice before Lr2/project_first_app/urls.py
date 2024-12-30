from django.urls import path
from . import views
from .views import CarDetailView, CarListView, add_owner, CarCreateView, CarUpdateView, CarDeleteView

urlpatterns = [
   path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
   path('owners/', views.owner_list_view, name='owner_list'),
   path('cars/', CarListView.as_view(), name='car_list'),
   path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
   path('add_owner/', add_owner, name='add_owner'),
   path('car/create/', CarCreateView.as_view(), name='car_create'),
   path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
   path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]

