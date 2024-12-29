from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AgentViewSet,
    OrganizationViewSet,
    ContractViewSet,
    InsuranceCaseViewSet,
    EmployeeViewSet,
    RelatedOrganizationsView,
    ContractsCountByTypeView,
    InsuredEmployeesView,
    TotalPayoutsByContractTypeView,
    ContractDetailsAndTotalPayoutsView,
    EmployeeContractViewSet,
    UserViewSet, AgentRegisterView, EmployeeRegisterView, DirectorRegisterView, UserProfileView, UserProfileUpdateView,
    ChangePasswordView, AgentDashboardView, DirectorDashboardView, EmployeeDashboardView,
    RegisterView, PositionViewSet, UserUpdateView, AgencyViewSet, ContractCreateView, UserPartialUpdateView
)

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'insurance_cases', InsuranceCaseViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'employee_contracts', EmployeeContractViewSet)
router.register(r'users', UserViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'agencies', AgencyViewSet)
urlpatterns = [
    path('', include(router.urls)),

    # Кастомные маршруты для дополнительных APIView и actions
    path('related_organizations/<int:organization_id>/', RelatedOrganizationsView.as_view(),
         name='related_organizations'),
    path('contracts_count/<str:start_date>/<str:end_date>/', ContractsCountByTypeView.as_view(),
         name='contracts_count_by_type'),
    path('insured_employees/<int:person_id>/', InsuredEmployeesView.as_view(),
         name='insured_employees'),
    path('total_payouts/<str:start_date>/<str:end_date>/', TotalPayoutsByContractTypeView.as_view(),
         name='total_payouts_by_contract_type'),
    path('contract_details/', ContractDetailsAndTotalPayoutsView.as_view(),
         name='contract_details_and_total_payouts'),

    path('contracts/<int:pk>/terminate/', ContractViewSet.as_view({'delete': 'terminate'}),
         name='terminate_contract'),

    path('agents/contracts_count_by_date/', AgentViewSet.as_view({'get': 'contracts_count_by_date'}),
         name='contracts_count_by_date'),
    path('employees/<int:pk>/fire/', EmployeeViewSet.as_view({'post': 'fire_employee'}),
         name='fire_employee'),
    path('users/me/', UserUpdateView.as_view(), name='user_update'),
    path('users/create/', UserViewSet.as_view({'post': 'create_user'}), name='create_user'),
    path('users/profile/', UserViewSet.as_view({'get': 'user_profile'}), name='user_profile'),
    path('contracts/<int:pk>/insurance_cases/', ContractViewSet.as_view({'get': 'insurance_case_summary'}),
         name='insurance_case_summary'),
    path('organizations/<int:pk>/agents/', OrganizationViewSet.as_view({'get': 'agents'}), name='organization_agents'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/agent/', AgentRegisterView.as_view(), name='register_agent'),
    path('register/employee/', EmployeeRegisterView.as_view(), name='register_employee'),
    path('register/director/', DirectorRegisterView.as_view(), name='register_director'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='update-profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('agent-dashboard/', AgentDashboardView.as_view(), name='agent-dashboard'),
    path('director-dashboard/', DirectorDashboardView.as_view(), name='director-dashboard'),
    path('employee-dashboard/', EmployeeDashboardView.as_view(), name='employee-dashboard'),
    path('contracts/', ContractCreateView.as_view(), name='create-contract'),
    path('profile/update-partial/', UserPartialUpdateView.as_view(), name='partial-update-profile'),

]
