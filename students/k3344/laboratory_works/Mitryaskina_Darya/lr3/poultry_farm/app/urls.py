from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    # Diet
    path('diets/', DietListView.as_view(), name='diet-list'),
    path('diets/<int:pk>/', DietDetailView.as_view(), name='diet-detail'),
    path('diets/create/', DietCreateView.as_view(), name='diet-create'),
    path('diets/<int:pk>/update/', DietUpdateView.as_view(), name='diet-update'),
    path('diets/<int:pk>/delete/', DietDeleteView.as_view(), name='diet-delete'),

    # Breed
    path('breeds/', BreedListView.as_view(), name='breed-list'),
    path('breeds/<int:pk>/', BreedDetailView.as_view(), name='breed-detail'),
    path('breeds/create/', BreedCreateView.as_view(), name='breed-create'),
    path('breeds/<int:pk>/update/', BreedUpdateView.as_view(), name='breed-update'),
    path('breeds/<int:pk>/delete/', BreedDeleteView.as_view(), name='breed-delete'),

    # Hen
    path('hens/', HenListView.as_view(), name='hen-list'),
    path('hens/<int:pk>/', HenDetailView.as_view(), name='hen-detail'),
    path('hens/create/', HenCreateView.as_view(), name='hen-create'),
    path('hens/<int:pk>/update/', HenUpdateView.as_view(), name='hen-update'),
    path('hens/<int:pk>/delete/', HenDeleteView.as_view(), name='hen-delete'),

    # Cage
    path('cages/', CageListView.as_view(), name='cage-list'),
    path('cages/<int:pk>/', CageDetailView.as_view(), name='cage-detail'),
    path('cages/create/', CageCreateView.as_view(), name='cage-create'),
    path('cages/<int:pk>/update/', CageUpdateView.as_view(), name='cage-update'),
    path('cages/<int:pk>/delete/', CageDeleteView.as_view(), name='cage-delete'),

    # Workshop
    path('workshops/', WorkshopListView.as_view(), name='workshop-list'),
    path('workshops/<int:pk>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('workshops/create/', WorkshopCreateView.as_view(), name='workshop-create'),
    path('workshops/<int:pk>/update/', WorkshopUpdateView.as_view(), name='workshop-update'),
    path('workshops/<int:pk>/delete/', WorkshopDeleteView.as_view(), name='workshop-delete'),

    # Employee
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    path('hens/eggs-count/', HenEggsCountView.as_view(), name='hen-eggs-count'),
    path('workshops/max-hen/', MaxHenByWorkshopView.as_view(), name='max-hen-by-workshop'),
    path('employees/avg-eggs/', AvgEggsPerEmployeeView.as_view(), name='avg-eggs-per-employee'),
    path('hens/count-by-breed-workshop/', HensCountByBreedAndWorkshopView.as_view(), name='hens-count-by-breed-workshop'),
    path('breeds/vs-factory-average/', BreedVsFactoryAverageView.as_view(), name='breed-vs-factory-average'),
]