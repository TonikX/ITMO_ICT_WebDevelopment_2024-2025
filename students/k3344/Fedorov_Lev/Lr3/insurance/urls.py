from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InsuranceAgencyViewSet, AgentViewSet, EmploymentContractViewSet,
    OrganizationViewSet, EmployeeViewSet, PositionViewSet,
    ContractViewSet, InsuranceCaseViewSet
)

router = DefaultRouter()
router.register(r'insurance-agencies', InsuranceAgencyViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'employment-contracts', EmploymentContractViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'insurance-cases', InsuranceCaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]