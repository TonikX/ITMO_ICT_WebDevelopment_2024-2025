from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_data, name='car_owner_data'),
    path('owner/list/', views.owners_list, name='car_owners_list'),
    path('car/<int:pk>/', views.CarData.as_view(), name='car_data'),
    path('car/<int:pk>/delete/', views.DeleteCar.as_view(), name='car_delete'),
    path('car/<int:pk>/update/', views.UpdateCar.as_view(), name='car_update'),
    path('car/list/', views.CarList.as_view(), name='car_list'),
    path('owner/add/', views.add_car_owner, name='add_car_owner'),
    path('car/add/', views.AddCar.as_view(), name='add_car'),
]