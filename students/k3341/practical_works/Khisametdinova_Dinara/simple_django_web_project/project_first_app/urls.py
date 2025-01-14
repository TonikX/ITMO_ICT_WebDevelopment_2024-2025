from django.urls import path
from . import views

urlpatterns = [
    path('owners', views.CarOwnerListView.as_view(), name='owner_list'),
    path('owner/<int:id>', views.owner_detail, name='owner_detail'),
    path('owner/create', views.CarOwnerCreateView.as_view(), name='create_owner'),
    path('owner/update/<int:pk>', views.CarOwnerUpdateView.as_view(), name="update_owner"),
    path('owner/delete/<int:pk>', views.CarOwnerDeleteView.as_view(), name="delete_owner"),

    path('cars', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car_detail'),
    path('car/create/', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
