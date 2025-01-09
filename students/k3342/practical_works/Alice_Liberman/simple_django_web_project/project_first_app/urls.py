from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('owner/', views.owners, name='owner'),
    path('owner/<int:id>/', views.owner_by_id, name='owner'),
    path('owner/create/', views.create_owner_view, name='cars_create'),
    path('cars/list/', views.CarsListVies.as_view(), name='cars'),
    path('cars/create/', views.CarCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/update', views.CarUpdateView.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete', views.CarDeleteView.as_view(), name='cars_delete'),
]

