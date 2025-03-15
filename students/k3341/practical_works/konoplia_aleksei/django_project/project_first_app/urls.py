from django.urls import path
from . import views

urlpatterns = [
    path('owners/', views.get_all_owners, name='owners-list'),
    path('owner/<int:owner_id>/', views.get_owner, name='owner-detail'),
    path('owner/create/', views.create_owner, name='owner-create'),
    path('cars/', views.ListOfCars.as_view(), name='cars-list'),
    path('car/<int:pk>/', views.RetrieveCarView.as_view(), name='car-detail'),
    path('car/create/', views.CreateCarView.as_view(), name='car-create'),
    path('car/<int:pk>/update/', views.UpdateCarView.as_view(), name='car-update'),
    path('car/<int:pk>/delete/', views.DeleteCarView.as_view(), name='car-delete'),
]
