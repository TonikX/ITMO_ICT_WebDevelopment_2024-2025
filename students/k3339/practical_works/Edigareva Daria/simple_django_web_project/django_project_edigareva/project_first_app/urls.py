from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('owners/', views.owner_list, name='owner_list'),
    path('licenses/', views.driving_license_list, name='license_list'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('car/add/', views.car_add, name='car_add'),
    path('car/<int:pk>/update/', views.car_update, name='car_update'),
    path('car/<int:pk>/delete/', views.car_delete, name='car_delete'),
    # path("signup/", views.SignUp.as_view(), name="signup"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('owners/<int:pk>/', views.owner_detail, name='owner_detail'),  # Detail view for owners
]

