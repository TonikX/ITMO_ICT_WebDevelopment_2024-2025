from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, create_owner_view, CarCreateView, CarDeleteView, register

urlpatterns = [
    path('', views.home, name='home'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owners/', views.owners_list, name='owners_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('owner/create/', create_owner_view, name='create_owner'),
path('car/create/', CarCreateView.as_view(), name='create_car'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='update_car'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='delete_car'),
    path('register/', register, name='register'),


]
