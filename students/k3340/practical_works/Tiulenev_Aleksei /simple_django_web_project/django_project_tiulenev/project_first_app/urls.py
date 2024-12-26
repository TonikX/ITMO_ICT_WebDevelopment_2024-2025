from django.urls import path
from . import views

urlpatterns = [
    path('owner_details/<int:owner_id>/', views.car_owner_detail, name='car_owner_detail'),
    path('time/', views.example_view),
    path('car/list', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/create', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update', views.CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete', views.CarDeleteView.as_view(), name='car_delete'),
    path('owner/list', views.CarOwnerListView.as_view(), name='owner_list'),
    path('owner/<int:pk>/', views.CarOwnerDetailView.as_view(), name='owner_detail'),
    path('owner/create', views.CarOwnerCreateView.as_view(), name='owner_create'),
    path('owner/<int:pk>/update', views.CarOwnerUpdateView.as_view(), name='owner_update'),
    path('owner/<int:pk>/delete', views.CarOwnerDeleteView.as_view(), name='owner_delete'),
]
