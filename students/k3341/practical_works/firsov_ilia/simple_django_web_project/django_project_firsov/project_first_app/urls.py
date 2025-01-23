from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/<int:pk>/', views.OwnerDetailView.as_view(), name='owner_detail'),
    path('licenses/', views.DrivingLicenseListView.as_view(), name='license_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/add/', views.CarCreateView.as_view(), name='car_add'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
