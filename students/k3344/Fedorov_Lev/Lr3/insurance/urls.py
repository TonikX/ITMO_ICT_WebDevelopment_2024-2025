from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AgentViewSet, OrganizationViewSet, ContractViewSet, InsuranceCaseViewSet,
                    EmployeeViewSet, RelatedOrganizationsView,
                    ContractsCountByTypeView, InsuredEmployeesView,
                    TotalPayoutsByContractTypeView, ContractDetailsAndTotalPayoutsView, EmployeeContractViewSet)

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'insurance_cases', InsuranceCaseViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'employee_contracts', EmployeeContractViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('related_organizations/<int:organization_id>/', RelatedOrganizationsView.as_view(), name='related_organizations'),
    path('contracts_count/<str:start_date>/<str:end_date>/', ContractsCountByTypeView.as_view(), name='contracts_count_by_type'),
    path('insured_employees/<int:person_id>/', InsuredEmployeesView.as_view(), name='insured_employees'),
    path('total_payouts/<str:start_date>/<str:end_date>/', TotalPayoutsByContractTypeView.as_view(), name='total_payouts_by_contract_type'),
    path('contract_details/', ContractDetailsAndTotalPayoutsView.as_view(), name='contract_details_and_total_payouts'),
]