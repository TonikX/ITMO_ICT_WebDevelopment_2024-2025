from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'workshops', CarWorkshopViewSet)
router.register(r'positions', JobPositionViewSet)
router.register(r'models', ModelViewSet)
router.register(r'automobiles', AutomobileViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'details', DetailViewSet)
router.register(r'car-details', CarDetailViewSet)
router.register(r'client-details', DetailsFromClientViewSet)
router.register(r'distribution', DistributionOfWorkViewSet)
router.register(r'detail-in-service', DetailInServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]