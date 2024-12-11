from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, add_car_owner, car_list, add_car, update_car, delete_car

urlpatterns = [
    path('owner/<int:owner_id>/', views.car_owner_detail, name='car_owner_detail'),
    path('owners/', views.owners_list, name='owners_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('add_car_owner/', add_car_owner, name='add_car_owner'),
    path('', car_list, name='car_list'),
    path('add/', add_car, name='add_car'),
    path('update/<int:car_id>/', update_car, name='update_car'),
    path('delete/<int:car_id>/', delete_car, name='delete_car'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

]
