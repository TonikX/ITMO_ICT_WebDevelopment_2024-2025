from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_details),
    path('owners/', views.owners),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car'),
    path('car/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
]