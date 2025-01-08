from django.urls import path
from . import views

urlpatterns = [
    path('owners/<int:owner_id>/', views.owner),
    path('owners/', views.owners),
    path('owners/create', views.create_owner, name='owner-create'),
    path('cars/', views.CarsList.as_view()),
    path('cars/create/', views.CarCreateView.as_view(), name="car-create"),
    path('cars/<int:car_id>/', views.CarRetrieveView.as_view(), name='car'),
    path('cars/<int:car_id>/update/', views.CarUpdateView.as_view(), name="car-update"),
    path('cars/<int:car_id>/delete/', views.CarDeleteView.as_view(), name="car-delete"),
]

