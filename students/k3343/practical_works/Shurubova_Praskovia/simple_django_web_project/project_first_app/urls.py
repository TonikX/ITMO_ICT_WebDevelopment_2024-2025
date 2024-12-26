from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView, add_owner


urlpatterns = [
    path('owner/<int:owner_id>/', views.detail),
    path('owner/', views.owners),
    path('cars/', CarListView.as_view(), name='cars'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_data'),
    path('owners/add/', add_owner, name='add_owner'),
    path('cars/add/', CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]
