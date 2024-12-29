from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CarViewSet, EmployeeViewSet,
    ServiceViewSet, OrderViewSet, OrderDetailsViewSet,
    PaymentViewSet, QualificationViewSet
)
from django.views.generic import TemplateView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'cars', CarViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailsViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'qualifications', QualificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
