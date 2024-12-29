from django.urls import path
from . import views
# from .views import CarsList, CarRetrieveView, CarUpdateView, create_owner, CarCreateView, \
#     CarDeleteView, CarsDeleteView

urlpatterns = [
    path('owners/<int:owner_id>/', views.owner, name='owner'),
    path('owners/', views.owners, name='owners'),
    path('cars/', views.CarsList.as_view(), name='cars'),
    path('cars/<int:pk>/', views.CarRetrieveView.as_view(), name='car'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('owners/create', views.create_owner, name='owner_create')
]

