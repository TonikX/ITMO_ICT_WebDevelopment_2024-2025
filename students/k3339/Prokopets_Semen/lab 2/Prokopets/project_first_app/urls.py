from django.urls import path
from . import views
from .views import example_view, owner_create, owner_list
from .views import CarListView, CarDetailView, CarUpdateView

urlpatterns = [

    path('cars/<int:car_id>/', views.cars),

    path('possession/', views.possessions),
    path('possession/<int:possession_id>/', views.possessions),
    path('owners/create/', owner_create, name='owner_create'),
    path('owners/', owner_list, name='owner_list'),
    path('drivelicense/', views.driveLicenses),
    path('drivelicens/<int:driveLicense_id>/', views.driveLicenses),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:car_id>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:car_id>/edit/', CarUpdateView.as_view(), name='car_update'),

    path('owner/', views.owners),
    path('owners/', views.owners_list),
    path('owner/<int:owner_id>/', views.owners),
    path('time/', example_view),
]


