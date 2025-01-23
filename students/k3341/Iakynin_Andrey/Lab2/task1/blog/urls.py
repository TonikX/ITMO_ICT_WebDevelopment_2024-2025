from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owner/list', views.owner_list, name='owner_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/',CarUpdateView.as_view(), name='car_update'),
    path('owner/add/', views.add_owner, name='owner_add'),
    path('cars/add/',CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]