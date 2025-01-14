from django.urls import path 
from . import views 

urlpatterns = [
    
    path('carOwner/<carOwner_id>/', views.get_carOwner), 
    path('carOwners/', views.carOwners), 
    path('owner/create/', views.create_owner_view), 
    path('car/<int:pk>/', views.CarView.as_view()),
    path('cars/', views.cars), 
    path('car/create/', views.CreateCar.as_view()), 
    path('car/<int:pk>/update/', views.UpdateCarView.as_view()), 
    path('car/<int:pk>/delete/', views.DeleteCarView.as_view()), 
]
