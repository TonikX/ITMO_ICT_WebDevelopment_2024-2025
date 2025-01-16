from django.urls import path 
from . import views

urlpatterns = [
    path('owners/<int:owner_id>/', views.get_owner_details),
    path('owners/', views.get_owners),
    path('owners/create/', views.create_owner),
    path('cars/', views.CarsList.as_view()),
    path('cars/<int:car_id>/', views.get_car_details),
    path('cars/create/', views.CreateCarView.as_view()),
    path('cars/<int:pk>/update/', views.UpdateCarView.as_view()),
    path('cars/<int:pk>/delete/', views.DeleteCarView.as_view()),
]
